# ZigmaNeural Assistant: Instant RAG Chatbot 🚀

ZigmaNeural Assistant is an instant, document-based AI assistant built as a Chrome Extension. It provides immediate answers from company documents with a high-performance backend designed for Vercel.

---

## 🌟 Key Features

- **Instant Responses**: Zero-latency retrieval from pre-processed document snippets.
- **Enterprise Glass UI**: A professional, dark, minimal interface integrated directly into the browser.
- **Vercel Powered**: High-speed, serverless backend with minimal cold starts compared to traditional hosting.
- **100% Private**: All document synthesis happens on your secure server instance.
- **Zero Running Costs**: Designed to run within Vercel's free tier quotas.

---

## 🛠️ Technical Setup

### 1. Backend Deployment (Vercel)
The backend engine handles document retrieval and provides instant replies.

1. **GitHub Upload**: Push the `rag_backend` directory (including `vercel.json` and `knowledge_base.json`) to your GitHub repository.
2. **Deploy on Vercel**:
   - Go to [vercel.com](https://vercel.com/) and import your repository.
   - Vercel will automatically detect the Python configuration and `vercel.json`.
   - Click **Deploy**.
3. **Finish**: Once deployed, copy your Vercel URL (e.g., `https://your-project.vercel.app`).

### 2. Frontend Installation (Chrome Extension)

1. **Build Project**: Navigate to `rar_frontend` and execute:
   ```bash
   npm run build
   ```
2. **Configure**: Update `BACKEND_URL` in `src/background.ts` to your Vercel URL.
3. **Load Extension**:
   - Navigate to `chrome://extensions` in Google Chrome.
   - Toggle **Developer Mode** on.
   - Click **Load unpacked** and select the `rar_frontend/dist` folder.

---

## 📂 Project Structure

```text
├── rag_backend/
│   ├── docs/                # Original source PDFs
│   ├── app.py               # FastAPI backend engine
│   ├── ingest.py            # Local processing script
│   ├── vercel.json          # Vercel deployment config
│   └── knowledge_base.json  # Pre-indexed knowledge data
└── rar_frontend/
    ├── src/                 # React source code
    └── dist/                # Production build files
```

---

## 📝 How to Use

1. Ensure your backend is deployed to Vercel.
2. Open any website in Chrome and click the ZigmaNeural icon.
3. Ask questions about the company, such as:
   - *"What is the leave policy?"*
   - *"Tell me about ZigmaNeural services."*

*Note: Answers are served instantly from the pre-loaded knowledge base.*
