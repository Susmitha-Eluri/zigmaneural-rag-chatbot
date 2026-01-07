import os
import json
from langchain_community.document_loaders import PyPDFLoader

# 100% FREE VERSION - NO EMBEDDINGS NEEDED
documents_data = []
docs_dir = "docs"

if not os.path.exists(docs_dir):
    print(f"❌ Error: {docs_dir} not found.")
    exit(1)

print("📂 Reading documents for Free Local Knowledge Base...")
for file in os.listdir(docs_dir):
    if file.endswith(".pdf"):
        file_path = os.path.join(docs_dir, file)
        try:
            loader = PyPDFLoader(file_path)
            pages = loader.load()
            text_content = "\n".join([p.page_content for p in pages])
            
            documents_data.append({
                "source": file,
                "content": text_content
            })
            print(f"📄 Read PDF: {file}")
            
        except Exception as e:
            print(f"⚠️ Failed to read {file}: {e}")

# Save to JSON for "Free Keyword RAG"
with open("knowledge_base.json", "w", encoding="utf-8") as f:
    json.dump(documents_data, f, indent=2)

print(f"✅ Created Free Knowledge Base with {len(documents_data)} documents.")
print("Now your AI can search these files for FREE!")
