// background.ts
chrome.runtime.onMessage.addListener((request: any, _sender: chrome.runtime.MessageSender, sendResponse: (response?: any) => void) => {
    if (request.type === "ASK_QUESTION") {
        const BACKEND_URL = "http://127.0.0.1:8001/ask";

        fetch(BACKEND_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: request.question })
        })
            .then(response => {
                if (!response.ok) throw new Error(`HTTP Error ${response.status}`);
                return response.json();
            })
            .then(data => {
                sendResponse({ success: true, answer: data.answer });
            })
            .catch(error => {
                console.error("Background Fetch Error:", error);
                sendResponse({ success: false, error: "Local Backend is not running on port 8001." });
            });

        return true;
    }
});
