// background.js
// Acts as a proxy to bypass Mixed Content restrictions (HTTPS page -> HTTP localhost)

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === "ASK_QUESTION") {

        const BACKEND_URL = "http://127.0.0.1:8001/ask";

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

        return true; // Keep the message channel open for async response
    }
});
