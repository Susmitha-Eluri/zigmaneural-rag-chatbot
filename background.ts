// background.ts
chrome.runtime.onMessage.addListener((request: any, _sender: chrome.runtime.MessageSender, sendResponse: (response?: any) => void) => {
    if (request.type === "ASK_QUESTION") {
        const BACKEND_URL = "https://zigmaneural-rag-chatbot.onrender.com/ask";

        // 60-second timeout for Render cold start
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 60000);

        fetch(BACKEND_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: request.question }),
            signal: controller.signal
        })
            .then(response => {
                clearTimeout(timeoutId);
                if (!response.ok) throw new Error(`HTTP Error ${response.status}`);
                return response.json();
            })
            .then(data => {
                sendResponse({ success: true, answer: data.answer });
            })
            .catch(error => {
                clearTimeout(timeoutId);
                console.error("Background Fetch Error:", error);
                let msg = "Backend is asleep or crashed. Check Render logs.";
                if (error.name === 'AbortError') msg = "Request timed out. Render is taking too long to wake up.";
                sendResponse({ success: false, error: msg });
            });

        return true;
    }
});
