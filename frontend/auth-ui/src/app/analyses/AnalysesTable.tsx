"use client";

import { useEffect, useState } from "react";

type Analysis = {
  id: number;
  name: string;
  createdAt: string;
};

export default function AnalysesTable() {
  const [analyses, setAnalyses] = useState<Analysis[]>([]);

  useEffect(() => {
    fetch("http://localhost:5000/analyses")  // backend URL
      .then(res => res.json())
      .then(data => setAnalyses(data));
  }, []);

  const handleDelete = async (id: number) => {
    await fetch(`http://localhost:5000/analyses/${id}`, {
      method: "DELETE",
    });
    setAnalyses(prev => prev.filter(a => a.id !== id));
  };

  return (
    <div>
      <h2>Analyses</h2>
      <table>
        <thead>
          <tr><th>ID</th><th>Name</th><th>Created At</th><th>Action</th></tr>
        </thead>
        <tbody>
          {analyses.map(a => (
            <tr key={a.id}>
              <td>{a.id}</td>
              <td>{a.name}</td>
              <td>{a.createdAt}</td>
              <td>
                <button onClick={() => handleDelete(a.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
