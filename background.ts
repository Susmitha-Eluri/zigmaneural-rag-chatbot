// background.ts
chrome.runtime.onMessage.addListener((request: any, _sender: chrome.runtime.MessageSender, sendResponse: (response?: any) => void) => {
    if (request.type === "ASK_QUESTION") {
        const BACKEND_URL = "http://localhost:8001/ask";

        fetch(BACKEND_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: request.question })
        })
            .then(response => response.json())
            .then(data => {
                sendResponse({ success: true, answer: data.answer });
            })
            .catch(error => {
                console.error("Background Fetch Error:", error);
                sendResponse({ success: false, error: error.message });
            });

        return true;
    }
});
