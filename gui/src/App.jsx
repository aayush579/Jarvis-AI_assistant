import React, { useState } from "react";

export default function App() {
  const [conversation, setConversation] = useState([]);
  const [input, setInput] = useState("");

  const send = async () => {
    if (!input.trim()) return;
    setConversation(c => [...c, {role: "user", text: input}]);
    // Placeholder: connect to FastAPI in future step.
    const reply = "(GUI placeholder) Connect this to FastAPI to talk to Jarvis.";
    setConversation(c => [...c, {role: "assistant", text: reply}]);
    setInput("");
  };

  return (
    <div style={{maxWidth: 700, margin: "40px auto", fontFamily: "system-ui"}}>
      <h1>Jarvis GUI</h1>
      <div style={{border:"1px solid #ddd", padding: 16, borderRadius: 12, minHeight: 240}}>
        {conversation.map((m, i) => (
          <div key={i} style={{margin: "8px 0"}}>
            <b>{m.role === "user" ? "You" : "Jarvis"}:</b> {m.text}
          </div>
        ))}
      </div>
      <div style={{display:"flex", gap:8, marginTop: 12}}>
        <input
          value={input}
          onChange={e=>setInput(e.target.value)}
          placeholder="Type a message..."
          style={{flex:1, padding:10, borderRadius:8, border:"1px solid #ccc"}}
        />
        <button onClick={send} style={{padding:"10px 16px", borderRadius:8}}>Send</button>
      </div>
      <p style={{marginTop:12, color:"#666"}}>Tip: Start the console Jarvis first. GUI is a scaffold you can extend.</p>
    </div>
  );
}
