from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore
from supabase.client import Client, create_client
from dotenv import load_dotenv
import os
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

# Config
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
embeddings = OpenAIEmbeddings()

# Initialize Vector Store
vector_store = SupabaseVectorStore(
    client=supabase,
    embedding=embeddings,
    table_name="documents",
    query_name="match_documents",
)

class Query(BaseModel):
    question: str

def search_knowledge_base(query: str, top_k: int = 7):
    """
    Search for documents using vector similarity in Supabase.
    """
    try:
        results = vector_store.similarity_search(query, k=top_k)
        if not results:
            return None
        
        context_str = ""
        for i, doc in enumerate(results, 1):
            source = doc.metadata.get("source", "Unknown")
            context_str += f"Snippet {i} (Source: {source}):\n{doc.page_content}\n\n"
        
        return context_str.strip()
    except Exception as e:
        print(f"❌ Supabase Search Error: {e}")
        return None

@app.post("/ask")
def ask(query: Query):
    # 1. Greetings
    greetings = {"hi", "hello", "hey", "good morning", "good evening"}
    clean_query = re.sub(r'[^\w\s]', '', query.question.lower().strip())
    if clean_query in greetings:
        return {
            "answer": "Hello! 👋 I’m here to help with questions about ZigmaNeural and its company policies.\n"
                      "What can I help you find today?"
        }

    # 2. Retrieval (Supabase Cloud)
    context = search_knowledge_base(query.question)
    
    # 3. Handle Missing Information
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
