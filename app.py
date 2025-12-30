from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

app = FastAPI()

# CORS (needed for Chrome extension)
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
    Search for keywords and return multiple relevant snippets.
    Includes synonym mapping and weighted relevance.
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
        raw_segments = re.split(r'\n\s*\n', doc["content"])
        
        for seg in raw_segments:
            seg = seg.strip()
            if not seg or len(seg) < 20: continue
            
            seg_lower = seg.lower()
            hits = 0
            found_words = 0
            
            # High Priority Keywords (if these match, they are likely the target)
            priority_keywords = {
                "leave": 20, "policy": 5, "vision": 15, "manufacturing": 15, 
                "voice": 15, "agent": 5, "contact": 20, "industries": 15,
                "workflow": 10, "automation": 10
            }

            for word in query_words:
                if re.search(fr"\b{re.escape(word)}\b", seg_lower):
                    found_words += 1
                    # Base weights
                    if word in ["zigmaneural", "novasoft"]:
                        hits += 0.1 # Very low weight for brand name (it's everywhere)
                    elif word in priority_keywords:
                        hits += priority_keywords[word]
                    else:
                        hits += 5.0 
            
            if found_words > 0:
                coverage_ratio = found_words / len(query_words)
                score = hits * (1 + coverage_ratio ** 2)
                
                # Authority Boost: If it's a general company query, favor the overview
                if is_brand_query and "overview" in doc["source"].lower():
                    score *= 3
                
                # Penalty: If they ask about "leave" and the snippet is IT security, penalize
                if "leave" in query_clean and "hr_policy" not in doc["source"].lower():
                    score *= 0.1

                if query_clean in seg_lower: 
                    score += 50
                
                if score > 5: # Threshold to filter out noise
                    all_matches.append({
                        "text": seg,
                        "hits": score,
                        "source": doc["source"]
                    })

    if not all_matches:
        return None

    # Sort by hits descending
    all_matches.sort(key=lambda x: -x['hits'])
    
    # Take top K and deduplicate by text
    seen = set()
    winners = []
    for match in all_matches:
        if match["text"] not in seen:
            winners.append(match)
            seen.add(match["text"])
        if len(winners) >= top_k:
            break

    # Format result
    context_str = ""
    for i, winner in enumerate(winners, 1):
        context_str += f"Snippet {i} (Source: {winner['source']}):\n{winner['text']}\n\n"
    
    return context_str.strip()

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

    # 2. Dynamic Load
    if not KNOWLEDGE_BASE and os.path.exists("knowledge_base.json"):
        with open("knowledge_base.json", "r", encoding="utf-8") as f:
            KNOWLEDGE_BASE = json.load(f)

    if not KNOWLEDGE_BASE:
        return {"answer": "❌ Knowledge Base empty. Run 'python ingest.py'."}

    # 3. Retrieval
    context = search_knowledge_base(query.question)
    if not context:
        return {"answer": "This information is not available in the provided company data."}

    # 4. AI Synthesis (STRICT 5-6 LINE RULE)
    try:
        llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
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
- Only answer what is explicitly asked.

Context:
{context}

Question: {query.question}
"""
        response = llm.invoke(prompt)
        answer = response.content.strip()
        
        # Final safety replace (case insensitive)
        answer = re.sub(r'novasoft', 'ZigmaNeural', answer, flags=re.I)
        
        # Extract unique sources
        sources = sorted(list(set(re.findall(r'\(Source: (.*?)\)', context))))
        source_str = ", ".join(sources)
        
        return {"answer": f"{answer}\n\n(Reference: {source_str})"}
        
    except Exception as e:
        # Fallback to direct summary (limited to ~5 lines)
        # Just use the first winner for fallback as it's the most relevant
        first_snippet = context.split('\n\n')[0]
        clean_ext = re.sub(r'Snippet \d+ \(Source: .*?\):', '', first_snippet).strip()
        sentences = re.split(r'(?<=[.!?])\s+', clean_ext)
        short_ext = " ".join(sentences[:5])
        if len(short_ext) > 300: short_ext = short_ext[:300] + "..."
        
        sources = sorted(list(set(re.findall(r'\(Source: (.*?)\)', context))))
        source_str = ", ".join(sources)
        return {"answer": f"{short_ext}\n\n(Source: {source_str})"}
