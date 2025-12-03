"use client";

import { useState } from "react";

export default function ExplainForm() {
  const [text, setText] = useState("");
  const [response, setResponse] = useState("");

  const handleSubmit = async () => {
    const res = await fetch("http://localhost:5000/cad/explain", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const data = await res.json();
    setResponse(data.explanation);
  };

  return (
    <div>
      <textarea onChange={e => setText(e.target.value)} placeholder="Çizim açıklaması"/>
      <button onClick={handleSubmit}>Gönder</button>
      <p>{response}</p>
    </div>
  );
}
