from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str

# Global knowledge base
KNOWLEDGE_BASE = []

def search_knowledge_base(query: str, top_k: int = 7):
    """
    Search for keywords and return relevant snippets (optimized for ZigmaNeural).
    """
    # Clean query
    query_clean = re.sub(r'^[a-z]+:\s*', '', query.lower())
    query_clean = re.sub(r'[^\w\s]', ' ', query_clean).strip()
    
    # Extract keywords
    query_words = set(re.findall(r'\w+', query_clean)) - {
        "what", "is", "the", "a", "an", "of", "in", "to", "for", "with", "on", "at", "by", "from", 
        "do", "does", "are", "which", "how", "tell", "me", "about", "can", "be", "used", "using", "ways", "should", "does"
    }
    
    # Synonym Mapping
    is_brand_query = False
    if "zigmaneural" in query_clean or "novasoft" in query_clean:
        is_brand_query = True
        query_words.add("novasoft")
        query_words.add("zigmaneural")

    if not query_words:
        return None

    all_matches = []
    for doc in KNOWLEDGE_BASE:
        # Split into blocks by double newline
        blocks = re.split(r'\n\s*\n', doc["content"])
        
        for block in blocks:
            block = block.strip()
            if not block or len(block) < 20: continue
            
            block_lower = block.lower()
            hits = 0
            found_words = 0
            
            # High Priority Keywords
            priority_keywords = {
                "leave": 20, "policy": 5, "vision": 15, "manufacturing": 15, 
                "voice": 15, "agent": 5, "contact": 20, "industries": 15,
                "workflow": 10, "automation": 10
            }

            for word in query_words:
                if re.search(fr"\b{re.escape(word)}\b", block_lower):
                    found_words += 1
                    if word in ["zigmaneural", "novasoft"]:
                        hits += 0.1 
                    elif word in priority_keywords:
                        hits += priority_keywords[word]
                    else:
                        hits += 5.0 
            
            if found_words > 0:
                coverage_ratio = found_words / len(query_words)
                score = hits * (1 + coverage_ratio ** 2)
                
                # Authority & Penalty
                if is_brand_query and "overview" in doc["source"].lower():
                    score *= 3
                if "leave" in query_clean and "hr_policy" not in doc["source"].lower():
                    score *= 0.1
                if query_clean in block_lower: 
                    score += 50
                
                if score > 5:
                    all_matches.append({
                        "text": block,
                        "hits": score,
                        "source": doc["source"]
                    })

    if not all_matches:
        return None

    # Sorting and Deduplication
    all_matches.sort(key=lambda x: -x['hits'])
    seen = set()
    winners = []
    for match in all_matches:
        if match["text"] not in seen:
            winners.append(match)
            seen.add(match["text"])
        if len(winners) >= top_k:
            break

    context_str = ""
    for i, winner in enumerate(winners, 1):
        context_str += f"Snippet {i} (Source: {winner['source']}):\n{winner['text']}\n\n"
    
    return context_str.strip()

@app.get("/health")
def health():
    return {"status": "ok", "docs": len(KNOWLEDGE_BASE)}

@app.post("/ask")
def ask(query: Query):
    global KNOWLEDGE_BASE
    
    # 1. Greetings
    greetings = {"hi", "hello", "hey", "good morning", "good evening"}
    clean_query = re.sub(r'[^\w\s]', '', query.question.lower().strip())
    if clean_query in greetings:
        return {
            "answer": "Hello! 👋 I’m here to help with questions about ZigmaNeural and its company policies.\n"
                      "What can I help you find today?"
        }

    # 2. Dynamic Data Load
    if not KNOWLEDGE_BASE and os.path.exists("knowledge_base.json"):
        with open("knowledge_base.json", "r", encoding="utf-8") as f:
            KNOWLEDGE_BASE = json.load(f)

    if not KNOWLEDGE_BASE:
        return {"answer": "❌ Knowledge Base is empty. Run 'python ingest.py' first!"}

    # 3. Retrieval
    context = search_knowledge_base(query.question)
    if not context:
        return {"answer": "This information is not available in the provided company data."}

    # 4. FREE Synthesis using Google Gemini
    try:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            return {"answer": "❌ Google API Key missing. Add GOOGLE_API_KEY to your settings."}
            
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key, temperature=0)
        
        prompt = f"""
You are the ZigmaNeural Assistant. 
The provided context contains snippets from internal documents.

STRICT RELEVANCE RULE:
- If the snippets do not contain the answer to the specific question, state: "This information is not available in the provided company data."
- Do NOT try to answer using general knowledge or unrelated snippets.

CRITICAL BRANDING RULES:
1. "NovaSoft" is our internal brand name. 
2. ALWAYS replace "NovaSoft" with "ZigmaNeural" in your answer.
3. NEVER mention "NovaSoft" to the user.

SYNTHESIS RULES:
- Answer based ONLY on the provided context.
- Your response MUST be exactly 5 to 6 lines long.
- Synthesize the facts into a professional, cohesive explanation.
- No headings, no bullet points, and no extra conversational filler.

Context:
{context}

Question: {query.question}
"""
        response = llm.invoke(prompt)
        answer = response.content.strip()
        answer = re.sub(r'novasoft', 'ZigmaNeural', answer, flags=re.I)
        
        # Sources
        sources = sorted(list(set(re.findall(r'\(Source: (.*?)\)', context))))
        source_str = ", ".join(sources)
        
        return {"answer": f"{answer}\n\n(Reference: {source_str})"}
        
    except Exception as e:
        print(f"❌ Gemini Error: {e}")
        return {"answer": "Sorry, I had trouble thinking. Please check your Google API Key settings."}
