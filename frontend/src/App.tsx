import { useState } from "react";
import "./App.css";

function App() {
  const [password, setPassword] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const analyzePassword = async () => {
    if (!password) return;

    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          password,
        }),
      });

      const data = await response.json();

      setResult(data);
    } catch (error) {
      console.log(error);
    }

    setLoading(false);
  };

  return (
    <div className="container">
      <div className="glass">
        <h1>Adaptive Credential Intelligence</h1>

        <p className="subtitle">
          AI-Powered Cybersecurity Password Intelligence Engine
        </p>

        <input
          type="password"
          placeholder="Enter secure password..."
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button onClick={analyzePassword}>
          {loading ? "Analyzing..." : "Analyze Password"}
        </button>

        {result && (
          <div className="result">
            <h2>Security Analysis</h2>

            <div className="card">
              <span>Strength</span>
              <strong>{result.strength}</strong>
            </div>

            <div className="card">
              <span>Security Score</span>
              <strong>{result.score}/100</strong>
            </div>

            <div className="card">
              <span>Entropy</span>
              <strong>{result.entropy}</strong>
            </div>

            <div className="card">
              <span>Breach Probability</span>
              <strong>{result.breach_probability}%</strong>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;