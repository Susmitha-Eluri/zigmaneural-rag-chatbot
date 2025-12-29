import os
import json
from langchain_community.document_loaders import PyPDFLoader, TextLoader

documents_data = []
docs_dir = "docs"

if not os.path.exists(docs_dir):
    print(f"❌ Error: {docs_dir} not found.")
    exit(1)

print("📂 Reading documents for Free Knowledge Base...")
for file in os.listdir(docs_dir):
    file_path = os.path.join(docs_dir, file)
    text_content = ""
    
    try:
        if file.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
            pages = loader.load()
            text_content = "\n".join([p.page_content for p in pages])
            print(f"📄 Read PDF: {file}")
            
        elif file.endswith(".txt"):
            loader = TextLoader(file_path, encoding='utf-8')
            docs = loader.load()
            text_content = "\n".join([d.page_content for d in docs])
            print(f"📄 Read TXT: {file}")
            
        if text_content:
            documents_data.append({
                "source": file,
                "content": text_content
            })
            
    except Exception as e:
        print(f"⚠️ Failed to read {file}: {e}")

# Save to JSON for "Free RAG"
with open("knowledge_base.json", "w", encoding="utf-8") as f:
    json.dump(documents_data, f, indent=2)

print(f"✅ Created Free Knowledge Base with {len(documents_data)} documents.")
print("Now run 'uvicorn app:app --reload --port 8001'")
