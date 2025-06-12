const backendUrl = "http://127.0.0.1:5000";

async function summarize() {
  const text = document.getElementById("text").value;
  const summaryEl = document.getElementById("summary");
  summaryEl.innerText = "Thinking...";

  try {
    const res = await fetch(`${backendUrl}/summarize`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ text }),
    });
    const data = await res.json();
    console.log("Backend response:", data);
    summaryEl.innerText = typeof data.summary === "string"
      ? data.summary
      : JSON.stringify(data.summary);
  } catch (e) {
    console.error(e);
    summaryEl.innerText = "Failed to fetch summary.";
  }
}

async function askQuestion() {
  const text = document.getElementById("text").value;
  const question = document.getElementById("question").value;
  const answerEl = document.getElementById("answer");
  answerEl.innerText = "Thinking...";

  try {
    const res = await fetch(`${backendUrl}/question`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ text, question }),
    });
    const data = await res.json();
    console.log("Backend response:", data);
    answerEl.innerText = typeof data.answer === "string"
      ? data.answer
      : JSON.stringify(data.answer);
  } catch (e) {
    console.error(e);
    answerEl.innerText = "Failed to fetch answer.";
  }
}
