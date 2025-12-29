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

1. Click the green **Code** button on this GitHub repository  
2. Select **Download ZIP**  
3. Once the ZIP file is downloaded, **unzip/extract** it to a folder on your computer  

---

## 🧩 How to Install the Extension in Chrome

1. Open **Google Chrome**
2. Go to: chrome://extensions
3. Turn ON **Developer mode** (top-right corner)
4. Click **Load unpacked**
5. Select the **unzipped project folder**
6. The ZigmaNeural AI extension will now appear in your extensions list

✅ At this stage, the chatbot UI will be visible.

---

## 💬 How to Use the Chatbot

1. Open the **ZigmaNeural website** in Chrome
2. Click on **Zigma Chat**, which appears at the bottom-right of the screen
3. A chatbot sidebar will appear on the page
4. Ask questions such as:
- *What is the company’s leave policy?*
- *What does ZigmaNeural do as a company?*
- *Which industries does ZigmaNeural serve with its AI solutions?*
- *What makes ZigmaNeural different from other AI companies?*
5. The chatbot responds **strictly using the provided documents**

---

## 🗂 Backend Setup (Required for AI Answers)

⚠️ **Important:**  
Installing the extension enables the **chatbot UI only**.  
To receive **real AI-generated answers**, the backend server must also be running.

The extension sends user questions to a local backend, which performs document retrieval and AI response generation using RAG.

### 1️⃣ Navigate to backend folder
```bash
cd rag_backend
2️⃣ Install backend dependencies
pip install -r requirements.txt

3️⃣ Start the backend server
uvicorn app:app --reload


The backend will run at:

http://127.0.0.1:8000


Once the backend is running, the chatbot will return full AI-powered answers.
