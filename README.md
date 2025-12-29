# ZigmaNeural AI Knowledge Base – Chrome Extension

This repository contains a Chrome extension that provides an AI-powered knowledge base chatbot for the **ZigmaNeural** website.  
The chatbot uses **Retrieval-Augmented Generation (RAG)** to answer questions strictly from company documents, services information, and HR policy PDFs—ensuring accurate, non-hallucinated responses.

---

## 🚀 What This Extension Does

- Adds an AI chatbot sidebar to the ZigmaNeural website
- Answers questions about:
  - Company overview
  - AI services & automation capabilities
  - Use cases and industries
  - HR policies (from uploaded PDFs)
- Uses document-based RAG (not generic internet answers)
- Designed as an **extension-first project**, easy to install and use

---

## 🧠 Tech Stack

- **Chrome Extension (Manifest V3)**
- **React + TypeScript**
- **Tailwind CSS**
- **shadcn/ui components**
- **FastAPI** (backend)
- **LangChain + FAISS** for document retrieval
- **LLM API** for answer generation

---

## 📦 How to Download the Extension

1. Click the green **Code** button on this GitHub repository.
2. Select **Download ZIP**.
3. Once the ZIP file is downloaded, **unzip/extract** it to a folder on your computer.

---

## 🧩 How to Install the Extension in Chrome

1. Open **Google Chrome**
2. Go to:  chrome://extensions
3. Turn ON **Developer mode** (top-right corner)
4. Click **Load unpacked**
5. Select the **unzipped project folder**
6. The ZigmaNeural AI extension will now appear in your extensions list

(Optional)  
- Click the puzzle icon 🧩 in the Chrome toolbar
- Pin the extension for easy access

---

## 💬 How to Use the Chatbot

1. Open the **ZigmaNeural website** in Chrome
2. Click on the **ZigmaNeural AI extension**
3. A chatbot sidebar will appear on the page
4. Ask questions such as:
- *What does ZigmaNeural do as a company?*
- *What is ZigmaNeural’s AI workflow automation?*
- *Which industries does ZigmaNeural serve?*
- *What is the company’s leave policy?*
5. The chatbot will respond using information from the provided documents only

---

## 🗂 Backend Setup (Required for AI Answers)

The extension connects to a local backend server for AI responses.

### 1️⃣ Navigate to backend folder
```bash
cd rag_backend
