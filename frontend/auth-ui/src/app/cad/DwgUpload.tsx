"use client";

import { useState } from "react";

export default function DwgUpload() {
  const [file, setFile] = useState<File | null>(null);

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("dwg", file);

    const res = await fetch("http://localhost:5000/cad/dwg", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    console.log(data);
  };

  return (
    <div>
      <input type="file" accept=".dwg" onChange={e => setFile(e.target.files?.[0] ?? null)} />
      <button onClick={handleUpload}>Upload DWG</button>
    </div>
  );
}
