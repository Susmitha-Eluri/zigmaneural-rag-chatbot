# ZigmaNeural Assistant: Decoupled AI Knowledge System 🚀

ZigmaNeural Assistant is a professional RAG (Retrieval-Augmented Generation) system. This setup uses a decoupled architecture for maximum performance and reliability.

- **Backend**: FastAPI running on **Railway** (Instant Keyword Retrieval).
- **Frontend**: Vite + React running on **Vercel** (Enterprise UI).
- **Client**: Chrome Extension (Directly calls the Railway API).

---

## 🛠️ Deployment Instructions

### 1. Backend Deployment (Railway)
1.  Push the **`rag_backend`** folder contents to a GitHub repository.
2.  Log in to [Railway](https://railway.app/).
3.  Click **"New Project"** > **"Deploy from GitHub repo"**.
4.  Select your repository. Railway will automatically detect the `Procfile` and `requirements.txt`.
5.  Wait for the build to finish. Once done, go to the **Settings** tab and click **"Generate Domain"** to get your API URL.

### 2. Frontend Deployment (Vercel)
1.  Push the **`rar_frontend`** folder contents to a GitHub repository.
2.  Log in to [Vercel](https://vercel.com/).
3.  Click **"Add New"** > **"Project"**.
4.  Import your repository. Vercel will auto-detect the Vite configuration.
5.  Click **"Deploy"**.

### 3. Extension Setup (Local Connection)
1.  Open `rar_frontend/src/background.ts`.
2.  Update the `BACKEND_URL` to your live **Railway URL** (add `/ask` at the end):
    ```typescript
    const BACKEND_URL = "https://your-railway-url.up.railway.app/ask";
    ```
3.  Run the build command in your terminal:
    ```bash
    cd rar_frontend
    npm run build
    ```
4.  Load the extension in Chrome via `chrome://extensions` using the `dist` folder.

---

## 📂 Project Structure

```text
├── rag_backend/         # Railway API
│   ├── app.py           # Backend Logic
│   ├── Procfile         # Deployment config
│   └── ...
└── rar_frontend/        # Vercel UI & Extension Source
    ├── src/             # React/TS source
    ├── dist/            # Built Extension
    └── ...
```

---

## 📝 How to Use
1. Ask a question through the Extension sidebar.
2. The Extension calls the Railway API.
3. Railway searches the local `knowledge_base.json` and returns the answer instantly.

*Note: This hybrid setup is optimized for zero-latency judging demos.*
