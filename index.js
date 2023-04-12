async function sendRequest() {
  const question = document.getElementsByName("user_input")[0].value;
  const response = await fetch('/ask_gpt4/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_input: question })
  });
  const data = await response.json();

  if (response.status === 200) {
    if ("response" in data) {
      const answerBox = document.createElement("code");
      answerBox.classList.add("d-block", "p-3", "bg-success", "text-white");
      answerBox.innerHTML = data.response.replace(/\n/g, "<br>");
      const answerElement = document.getElementById("answer");
      while (answerElement.firstChild) {
        answerElement.removeChild(answerElement.firstChild);
      }
      answerElement.appendChild(answerBox);
    } else if ("error" in data) {
      document.getElementById("answer").innerHTML = `Error: ${data.error}`;
    } else {
      document.getElementById("answer").innerHTML = "Unknown error.";
    }
  } else {
    document.getElementById("answer").innerHTML = "Server error.";
  }
}
