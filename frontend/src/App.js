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
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
        <textarea
          rows={4}
          style={{ width: "100%", padding: 8 }}
          placeholder="Enter patient's symptoms and history..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          required
        />
        <div style={{ display: 'flex', gap: 12 }}>
          <button type="submit" style={{ marginTop: 12, padding: "8px 24px", background: '#4CAF50', color: '#fff', border: 'none', borderRadius: 5, cursor: 'pointer' }} disabled={loading}>
            {loading ? "Analyzing..." : "Analyze"}
          </button>
          <button type="button" style={{ marginTop: 12, padding: "8px 24px", background: '#eee', color: '#333', border: '1px solid #bbb', borderRadius: 5, cursor: 'pointer' }} onClick={() => { setInput(""); setResult(null); setError(""); }} disabled={loading}>
            Reset
          </button>
        </div>
      </form>
      {error && <div style={{ color: "red", marginTop: 16 }}>{error}</div>}
      {result && (
        <div style={{ marginTop: 24, background: "#f7f7f7", padding: 16, borderRadius: 8 }}>
          <h3>Results</h3>
          <b>Parsed Symptoms:</b> {result.parsed_symptoms && result.parsed_symptoms.length > 0 ? result.parsed_symptoms.join(", ") : <span style={{ color: 'green' }}>None detected</span>}
          <br /><br />
          {result.comorbidities && (
            <>
              <b>Comorbidities:</b> {result.comorbidities.length > 0 ? result.comorbidities.join(", ") : <span style={{ color: 'green' }}>None</span>}
              <br /><br />
            </>
          )}
          <b>Top Diagnoses:</b>
          <ul>
            {result.diagnoses && result.diagnoses.map((d, i) => (
              <li key={i}>{d.disease} (matches: {d.count})</li>
            ))}
          </ul>
          {result.differentials && (
            <>
              <b>Differential Diagnoses:</b>
              <ul>
                {result.differentials.length > 0 ? result.differentials.map((d, i) => <li key={i}>{typeof d === 'object' ? JSON.stringify(d) : d}</li>) : <li>None</li>}
              </ul>
            </>
          )}
          <b>Treatments:</b>
          <ul>
            {result.treatments && result.treatments.map((t, i) => (
              <li key={i}>{t.disease}: {t.treatment}</li>
            ))}
          </ul>
          {result.red_flags && result.red_flags.length > 0 && (
            <>
              <b style={{ color: 'red' }}>Red Flags:</b>
              <ul>
                {result.red_flags.map((rf, i) => (
                  <li key={i} style={{ color: 'red', fontWeight: 'bold' }}>{rf}</li>
                ))}
              </ul>
            </>
          )}
          {result.guidelines && (
            <>
              <b>Guidelines:</b>
              <ul>
                {Array.isArray(result.guidelines)
                  ? result.guidelines.map((g, i) => (
                      typeof g === 'object'
                        ? Object.entries(g).map(([k, v]) => <li key={k}>{k}: {v}</li>)
                        : <li key={i}>{g}</li>
                    ))
                  : typeof result.guidelines === 'object'
                    ? Object.entries(result.guidelines).map(([k, v]) => <li key={k}>{k}: {v}</li>)
                    : <li>{result.guidelines}</li>}
              </ul>
            </>
          )}
          <b>Assessment:</b> <span style={{ color: result.assessment.urgent ? "red" : "green" }}>
            {result.assessment.message}
          </span>
        </div>
      )}
    </div>
  );
}

export default App;
