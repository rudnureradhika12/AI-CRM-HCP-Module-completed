import React, { useState } from "react";
import "./index.css";

export default function App() {

  // ===== CHAT STATE =====
  const [chat, setChat] = useState([
    { role: "agent", text: "Hello! Describe your HCP interaction." }
  ]);
  const [msg, setMsg] = useState("");

  // ===== FORM STATE =====
  const [hcpId, setHcpId] = useState("HCP-001");
  const [interactionType, setInteractionType] = useState("Visit");
  const [notes, setNotes] = useState("");
  const [saved, setSaved] = useState(false);
  const [tags, setTags] = useState([]);

  const API_URL = "http://127.0.0.1:8000/api/interactions/";
  const CHAT_URL = "http://127.0.0.1:8000/api/chat";

  // ================================
  // SAVE INTERACTION
  // ================================
  const saveInteraction = async () => {

    if (!hcpId || !interactionType || !notes) {
      alert("Fill all fields before saving.");
      return;
    }

    const payload = {
      hcp_id: hcpId,
      rep_id: "REP-001",
      interaction_type: interactionType,
      notes,
      metadata: {}
    };

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      const data = await res.json();

      if (!res.ok) {
        alert("Backend Error: " + JSON.stringify(data.detail || data));
        return;
      }

      setSaved(true);
      setTags(["Follow-Up", "Prescription", "Product Interest"]);
      alert("Interaction saved ✅");

    } catch (err) {
      alert("Save failed: " + err.message);
    }
  };


  // ================================
  // SEND MESSAGE TO AI
  // ================================
  const sendMessage = async () => {

    if (!msg.trim()) return;

    const userMessage = { role: "user", text: msg };
    setChat(prev => [...prev, userMessage]);
    setMsg("");

    try {
      const res = await fetch(CHAT_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: msg })
      });

      const data = await res.json();

      const aiMessage = { role: "agent", text: data.reply };
      setChat(prev => [...prev, aiMessage]);

      // Auto-fill notes from AI if you want:
      // setNotes(data.reply);

    } catch {
      setChat(prev => [...prev, { role: "agent", text: "AI backend not responding." }]);
    }
  };


  return (
    <div className="container">

      <h1>AI-First CRM — HCP Module</h1>

      <div className="grid">

        {/* ================= FORM CARD ================= */}
        <div className="card" style={{ height: "500px", overflow: "hidden" }}>
          <h2>Log Interaction</h2>

          <div className="field">
            <label>HCP ID</label>
            <input value={hcpId} onChange={e => setHcpId(e.target.value)} />
          </div>

          <div className="field">
            <label>Interaction Type</label>
            <select value={interactionType} onChange={e => setInteractionType(e.target.value)}>
              <option>Visit</option>
              <option>Call</option>
              <option>Email</option>
            </select>
          </div>

          <div className="field">
            <label>Notes</label>
            <textarea rows="5" value={notes} onChange={e => setNotes(e.target.value)} />
          </div>

          <button className="primary" onClick={saveInteraction}>
            Save Interaction
          </button>

          {saved && (
            <div className="history">
              <b>Auto-tags:</b>
              {tags.map(t => (
                <span key={t} className="tag">#{t}</span>
              ))}
            </div>
          )}
        </div>


        {/* ================= CHAT CARD ================= */}
        <div className="card" style={{ height: "500px", display: "flex", flexDirection: "column" }}>
          <h2>AI Assistant</h2>

          <div
            className="chatBox"
            style={{
              flex: 1,
              overflowY: "auto",
              marginBottom: "10px"
            }}
          >
            {chat.map((m, i) => (
              <div key={i} className={m.role === "user" ? "chatUser" : "chatAgent"}>
                <b>{m.role === "user" ? "You" : "AI"}:</b> {m.text}
              </div>
            ))}
          </div>

          <div className="chatInput" style={{ display: "flex", gap: "10px" }}>
            <input
              style={{ flex: 1 }}
              placeholder="Ask AI about interaction..."
              value={msg}
              onChange={e => setMsg(e.target.value)}
            />
            <button className="primary" onClick={sendMessage}>
              Send
            </button>
          </div>

        </div>

      </div>
    </div>
  );
}
