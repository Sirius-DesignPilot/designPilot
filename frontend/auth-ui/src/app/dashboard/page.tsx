"use client";

import { useEffect, useState } from "react";

export default function DashboardPage() {
  const [lastAnalysis, setLastAnalysis] = useState<string>("");

  useEffect(() => {
    fetch("http://localhost:5000/dashboard/stats")
      .then(res => res.json())
      .then(data => setLastAnalysis(data.lastAnalysisTime));
  }, []);

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Last Analysis: {lastAnalysis}</p>
    </div>
  );
}
