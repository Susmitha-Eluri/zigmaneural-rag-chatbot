(() => {
  const SIDEBAR_WIDTH = 320;
  const BACKEND_URL = "http://127.0.0.1:8001/ask";

  // Prevent duplicate injection
  if (document.getElementById("ai-chat-toggle")) return;

  let sidebarOpen = false;

  // ===============================
  // Toggle Button
  // ===============================
  const toggleBtn = document.createElement("div");
  toggleBtn.id = "ai-chat-toggle";
  toggleBtn.innerText = "Zigma Chat";
  toggleBtn.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: #4F46E5;
    color: white;
    padding: 10px 14px;
    border-radius: 20px;
    cursor: pointer;
    font-size: 14px;
    z-index: 999999;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
  `;
  document.body.appendChild(toggleBtn);

  // ===============================
  // Sidebar
  // ===============================
  const sidebar = document.createElement("div");
  sidebar.id = "ai-knowledge-sidebar";
  sidebar.style.cssText = `
    position: fixed;
    top: 0;
    right: 0;
    width: ${SIDEBAR_WIDTH}px;
    height: 100vh;
    background: #0f172a;
    color: #e5e7eb;
    z-index: 999998;
    font-family: Arial, sans-serif;
    display: none;
    flex-direction: column;
    box-shadow: -3px 0 10px rgba(0,0,0,0.4);
  `;

  sidebar.innerHTML = `
    <div style="
      padding:12px;
      border-bottom:1px solid #334155;
      display:flex;
      justify-content:space-between;
      align-items:center;
    ">
      <div>
        <b>ZigmaNeural Assistant</b>
        <div style="font-size:12px;color:#94a3b8;">
          Ask company documents
        </div>
      </div>
      <span id="close-ai" style="cursor:pointer;font-size:18px;">✖</span>
    </div>

    <div id="chat-area" style="
      flex:1;
      padding:12px;
      overflow-y:auto;
      font-size:14px;
    ">
      <div style="color:#94a3b8;">
        👋 Ask a question to get answers from company knowledge.
      </div>
    </div>

    <div style="padding:12px;border-top:1px solid #334155;">
      <textarea id="question-input"
        placeholder="Type your question..."
        style="
          width:100%;
          height:60px;
          resize:none;
          padding:8px;
          border-radius:6px;
          border:1px solid #334155;
          background:#1e293b;
          color:#f8fafc;
          outline:none;
          font-size:14px;
        "></textarea>

      <button id="ask-btn"
        style="
          margin-top:8px;
          width:100%;
          padding:8px;
          background:#4F46E5;
          color:white;
          border:none;
          border-radius:6px;
          cursor:pointer;
          font-size:14px;
        ">
        Ask
      </button>
    </div>
  `;

  document.body.appendChild(sidebar);

  const chatArea = sidebar.querySelector("#chat-area");
  const input = sidebar.querySelector("#question-input");
  const askBtn = sidebar.querySelector("#ask-btn");
  const closeBtn = sidebar.querySelector("#close-ai");

  // ===============================
  // Open / Close Logic
  // ===============================
  toggleBtn.onclick = () => {
    if (sidebarOpen) return;
    sidebar.style.display = "flex";
    document.documentElement.style.marginRight = SIDEBAR_WIDTH + "px";
    sidebarOpen = true;
  };

  closeBtn.onclick = () => {
    sidebar.style.display = "none";
    document.documentElement.style.marginRight = "0px";
    sidebarOpen = false;
  };

  // ===============================
  // Chat Logic (REAL BACKEND CALL)
  // ===============================
  askBtn.onclick = async () => {
    const question = input.value.trim();
    if (!question) return;

    // User message
    const userMsg = document.createElement("div");
    userMsg.style.cssText = `
      margin:8px 0;
      padding:8px;
      background:#4F46E5;
      color:white;
      border-radius:6px;
    `;
    userMsg.innerText = "You: " + question;
    chatArea.appendChild(userMsg);

    input.value = "";

    // Bot placeholder
    const botMsg = document.createElement("div");
    botMsg.style.cssText = `
      margin:8px 0;
      padding:8px;
      background:#1e293b;
      border-radius:6px;
      color:#e2e8f0;
    `;
    botMsg.innerText = "AI: Thinking...";
    chatArea.appendChild(botMsg);

    chatArea.scrollTop = chatArea.scrollHeight;

    try {
      if (!chrome.runtime || !chrome.runtime.sendMessage) {
        throw new Error("Extension context invalidated. Please refresh the page (F5) to continue.");
      }

      // Send message to background script (to bypass Mixed Content issues)
      chrome.runtime.sendMessage(
        { type: "ASK_QUESTION", question: question },
        (response) => {
          if (chrome.runtime && chrome.runtime.lastError) {
            botMsg.innerText = "❌ Extension Error: " + chrome.runtime.lastError.message + " (Please refresh the page)";
            return;
          }

          if (response && response.success) {
            botMsg.innerText = "AI: " + response.answer;
          } else {
            botMsg.innerText =
              "❌ Could not connect to backend.\n" +
              "Make sure FastAPI server is running at http://127.0.0.1:8001";
          }
          chatArea.scrollTop = chatArea.scrollHeight;
        }
      );

    } catch (err) {
      botMsg.innerText = "❌ Connection Error: " + err.message;
      if (err.message.includes("invalidated")) {
        botMsg.innerText += "\n\n(This happens after an extension update. Just press F5 to fix it!)";
      }
    }

    chatArea.scrollTop = chatArea.scrollHeight;
  };
})();
