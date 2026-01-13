import React, { useEffect, useState } from "react";
import { fetchInsights, sendChatQuestion } from "./api";
import "./App.css";

function App() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loadingChat, setLoadingChat] = useState(false);

  useEffect(() => {
    fetchInsights()
      .then((res) => setData(res))
      .catch((err) => setError(err.message));
  }, []);

  const handleAsk = async () => {
    if (!question.trim()) return;

    setLoadingChat(true);
    setAnswer("");

    try {
      const res = await sendChatQuestion(question);
      setAnswer(res.recommendation);
    } catch (err) {
      setAnswer("Unable to fetch recommendation. Backend may be unavailable.");
    } finally {
      setLoadingChat(false);
    }
  };

  if (error) {
    return <div className="container error">Backend error: {error}</div>;
  }

  if (!data) {
    return <div className="container">Loading analytics...</div>;
  }

  return (
    <div className="container">
      <h1>Retail Footfall Analytics Dashboard</h1>

      {/* KPIs */}
      <section>
        <h2>Key Metrics</h2>
        <ul>
          <li>Total Visitors: <b>{data.kpis.total_visitors}</b></li>
          <li>Average Daily Footfall: <b>{data.kpis.avg_daily_footfall}</b></li>
          <li>Average Session Time (sec): <b>{data.kpis.avg_session_seconds}</b></li>
          <li>Peak Hour: <b>{data.kpis.peak_hour}:00</b></li>
        </ul>
      </section>

      {/* Pareto */}
      <section>
        <h2>Pareto Insight</h2>
        <p>
          Top <b>{data.pareto.top_hours_percentage}%</b> of hours contribute to
          <b> 80%</b> of total footfall.
        </p>
      </section>

      {/* Trend */}
      <section>
        <h2>Demand Trend</h2>
        <p>Status: <b>{data.trend.interpretation}</b></p>
        <p>Slope: <b>{data.trend.slope}</b></p>
      </section>

      {/* LLM CHAT */}
      <section>
        <h2>AI Recommendation (Chat)</h2>

        <input
          type="text"
          value={question}
          placeholder="Ask a business question (e.g. staffing recommendation)"
          onChange={(e) => setQuestion(e.target.value)}
          style={{ width: "100%", padding: "8px", marginBottom: "10px" }}
        />

        <button onClick={handleAsk} disabled={loadingChat}>
          {loadingChat ? "Thinking..." : "Ask AI"}
        </button>

        {answer && (
          <div style={{ marginTop: "15px", background: "#f4f6f8", padding: "10px" }}>
            <b>Recommendation:</b>
            <p>{answer}</p>
          </div>
        )}
      </section>
    </div>
  );
}

export default App;
