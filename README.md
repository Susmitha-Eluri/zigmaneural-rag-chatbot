# ZigmaNeural Assistant: Enterprise RAG Chatbot 🚀
ZigmaNeural Assistant is an advanced AI knowledge base designed as a Chrome Extension. It leverages **Retrieval-Augmented Generation (RAG)** to provide accurate, document-based responses directly within your browser.
---
## 🌟 Key Features
- **Document-Centric AI**: Intelligent responses synthesized exclusively from your company documents.
- **Enterprise Glass UI**: A professional, dark, minimal interface that integrates seamlessly into any web environment.
- **Efficiency Optimized**: Powered by Google Gemini 1.5 Flash for rapid response times and high-quality synthesis.
- **Secure & Private**: Operates using internal document indexing, strictly following enterprise data boundaries.
- **Zero Infrastructure Costs**: Lightweight architecture that runs without the need for expensive vector databases.
---
## 🛠️ Technical Setup
### 1. Backend Deployment (Render)
The backend engine handles document retrieval and AI synthesis.
1. **Deployment**: Push the `rag_backend` directory to your GitHub repository.
2. **Setup on Render**: Create a new **Web Service**.
   - **Root Directory**: `rag_backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app`
3. **Configuration**: Add `GOOGLE_API_KEY` as an environment variable (from [Google AI Studio](https://aistudio.google.com/)).
### 2. Frontend Installation (Chrome Extension)
1. **Build Project**: Navigate to `rar_frontend` and execute:
   ```bash
   npm run build
Load Extension:
Navigate to chrome://extensions in Google Chrome.
Toggle Developer Mode on.
Click Load unpacked and select the rar_frontend/dist folder.
Network Configuration: Ensure BACKEND_URL in src/background.ts matches your active Render service address.
📂 Project Structure
├── rag_backend/
│   ├── docs/                # Knowledge base source files (PDFs)
│   ├── app.py               # FastAPI engine & AI logic
│   ├── ingest.py            # Local document processing script
│   ├── knowledge_base.json  # Indexed knowledge data
│   └── requirements.txt     # Service dependencies
└── rar_frontend/
    ├── src/                 # React application source
    ├── dist/                # Production build files
    └── public/              # Static assets & manifest.json
📝 Usage Guide
Knowledge Base: The system comes pre-loaded with official company documents in rag_backend/docs.
Indexing: To update or verify document indexing, run:
python ingest.py
Sync: Push updates to GitHub and reload the extension in Chrome.
Interaction: Ask context-specific questions such as:
"What is the ZigmaNeural leave policy?"
"What are the core services provided by ZigmaNeural?"
✅ Summary
Built for the modern enterprise, the ZigmaNeural Assistant transforms static company documents into an interactive goldmine of information, accessible instantly from any browser tab.
