async function sendMessage() {

  const input = document.getElementById("userInput");
  const msg = input.value;

  addMessage("user", msg);

  const response = await fetch("http://127.0.0.1:8000/api/chat", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({message: msg})
  });

  const data = await response.json();
  addMessage("agent", data.reply);
  input.value = "";
}

function addMessage(type, text) {
  const chat = document.getElementById("chat");

  const bubble = document.createElement("div");
  bubble.className = type === "user" ? "user-msg" : "agent-msg";

  bubble.textContent = text;
  chat.appendChild(bubble);
}
