from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import json
import re

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

def search_knowledge_base(query: str, top_k_sentences: int = 3):
    """
    Search for keywords at the sentence level and return a concise answer (Instantly).
    """
    # Clean query
    query_clean = re.sub(r'^[a-z]+:\s*', '', query.lower())
    query_clean = re.sub(r'[^\w\s]', ' ', query_clean).strip()
    
    # Extract keywords
    query_words = set(re.findall(r'\w+', query_clean)) - {
        "what", "is", "the", "a", "an", "of", "in", "to", "for", "with", "on", "at", "by", "from", 
        "do", "does", "are", "which", "how", "tell", "me", "about", "can", "be", "used", "using", "ways", "should", "does"
    }
    
    if not query_words:
        return None

    all_sentence_matches = []
    for doc in KNOWLEDGE_BASE:
        # Split content into sentences using regex (handles . ! ?)
        sentences = re.split(r'(?<=[.!?])\s+', doc["content"])
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence or len(sentence) < 15: continue
            
            sentence_lower = sentence.lower()
            hits = 0
            found_words = 0
            
            priority_keywords = {
                "leave": 25, "policy": 10, "vision": 15, "manufacturing": 15, 
                "voice": 15, "agent": 10, "contact": 25, "industries": 15,
                "workflow": 10, "automation": 10, "benefits": 20, "security": 20
            }

            for word in query_words:
                if re.search(fr"\b{re.escape(word)}\b", sentence_lower):
                    found_words += 1
                    if word in priority_keywords:
                        hits += priority_keywords[word]
                    else:
                        hits += 10.0 
            
            if found_words > 0:
                # Bonus for exact query match in sentence
                if query_clean in sentence_lower:
                    hits += 50
                
                # Coverage ratio (how much of the query is in this sentence)
                coverage = found_words / len(query_words)
                score = hits * (1 + coverage)
                
                all_sentence_matches.append({
                    "text": sentence,
                    "hits": score,
                    "source": doc["source"]
                })

    if not all_sentence_matches:
        return None

    # Sort sentences by score
    all_sentence_matches.sort(key=lambda x: -x['hits'])
    
    # Pick top unique sentences from the same context if possible
    selected_sentences = []
    seen_text = set()
    sources = set()
    
    for match in all_sentence_matches:
        if match["text"] not in seen_text:
            selected_sentences.append(match["text"])
            seen_text.add(match["text"])
            sources.add(match["source"])
        if len(selected_sentences) >= top_k_sentences:
            break

    # Assemble and clean answer
    answer = " ".join(selected_sentences)
    answer = re.sub(r'\s+', ' ', answer).strip()
    
    # Branding replace
    answer = re.sub(r'novasoft', 'ZigmaNeural', answer, flags=re.I)
    
    source_str = ", ".join(sorted(list(sources)))
    return f"{answer}\n\n(Source: {source_str})"

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
            "answer": "Hello! 👋 I am the ZigmaNeural Assistant. I can quickly answer questions about our company policies and services. What would you like to know?"
        }

    # 2. Dynamic Data Load
    current_dir = os.path.dirname(os.path.abspath(__file__))
    kb_path = os.path.join(current_dir, "knowledge_base.json")
    
    if not KNOWLEDGE_BASE and os.path.exists(kb_path):
        with open(kb_path, "r", encoding="utf-8") as f:
            KNOWLEDGE_BASE = json.load(f)

    if not KNOWLEDGE_BASE:
        return {"answer": "❌ Knowledge Base is empty. Please run 'python ingest.py' first!"}

    # 3. Instant Concise Retrieval
    answer = search_knowledge_base(query.question)
    if not answer:
        return {"answer": "I'm sorry, I couldn't find a specific answer to that in the company records."}

    return {"answer": answer}
