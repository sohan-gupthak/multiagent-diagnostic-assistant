import React, { useState } from "react";
import axios from "axios";

function App() {
  const [input, setInput] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const res = await axios.post("http://localhost:5050/api/diagnose", {
        user_input: input,
      });
      setResult(res.data);
    } catch (err) {
      setError("Error connecting to backend");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h2>AI Diagnostic Assistant</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          rows={4}
          style={{ width: "100%", padding: 8 }}
          placeholder="Enter patient's symptoms and history..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          required
        />
        <button type="submit" style={{ marginTop: 12, padding: "8px 24px" }}>
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </form>
      {error && <div style={{ color: "red", marginTop: 16 }}>{error}</div>}
      {result && (
        <div style={{ marginTop: 24, background: "#f7f7f7", padding: 16, borderRadius: 8 }}>
          <h3>Results</h3>
          <b>Parsed Symptoms:</b> {result.parsed_symptoms.join(", ")}
          <br /><br />
          <b>Top Diagnoses:</b>
          <ul>
            {result.diagnoses.map((d, i) => (
              <li key={i}>{d.disease} (matches: {d.count})</li>
            ))}
          </ul>
          <b>Treatments:</b>
          <ul>
            {result.treatments.map((t, i) => (
              <li key={i}>{t.disease}: {t.treatment}</li>
            ))}
          </ul>
          <b>Assessment:</b> <span style={{ color: result.assessment.urgent ? "red" : "green" }}>
            {result.assessment.message}
          </span>
        </div>
      )}
    </div>
  );
}

export default App;
