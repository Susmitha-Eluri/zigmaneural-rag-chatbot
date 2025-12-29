document.getElementById("askBtn").addEventListener("click", async () => {
  const question = document.getElementById("question").value;
  const answerDiv = document.getElementById("answer");

  // Replace URL below with your RAG backend API endpoint
  const response = await fetch("https://your-rag-server.com/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question: question })
  });

  const data = await response.json();
  answerDiv.innerText = data.answer || "No answer found.";
});
