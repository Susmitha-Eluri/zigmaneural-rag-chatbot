import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore
from supabase.client import Client, create_client
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# Config
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

if not all([SUPABASE_URL, SUPABASE_KEY, OPENAI_API_KEY]):
    print("❌ Error: Missing environment variables (SUPABASE_URL, SUPABASE_KEY, OPENAI_API_KEY).")
    exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
embeddings = OpenAIEmbeddings()

docs_dir = "docs"
if not os.path.exists(docs_dir):
    print(f"❌ Error: {docs_dir} not found.")
    exit(1)

print("📂 Reading documents for Supabase Cloud RAG...")
all_chunks = []
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

for file in os.listdir(docs_dir):
    if file.endswith(".pdf"):
        file_path = os.path.join(docs_dir, file)
        try:
            loader = PyPDFLoader(file_path)
            pages = loader.load()
            # Split pages into chunks
            chunks = text_splitter.split_documents(pages)
            for chunk in chunks:
                chunk.metadata["source"] = file
            all_chunks.extend(chunks)
            print(f"📄 Processed PDF: {file} ({len(chunks)} chunks)")
        except Exception as e:
            print(f"⚠️ Failed to read {file}: {e}")

if not all_chunks:
    print("❌ No chunks created. Check your PDF documents.")
    exit(1)

print(f"📤 Pushing {len(all_chunks)} chunks to Supabase...")
try:
    vector_store = SupabaseVectorStore.from_documents(
        all_chunks,
        embeddings,
        client=supabase,
        table_name="documents",
        query_name="match_documents",
    )
    print("✅ Successfully updated Supabase Vector Store.")
except Exception as e:
    print(f"❌ Failed to push to Supabase: {e}")
    print("💡 TIP: Make sure you have created the 'documents' table and 'match_documents' function in Supabase.")
