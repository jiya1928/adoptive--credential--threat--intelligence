import "./App.css";
import axios from "axios";
import { useState } from "react";
import axios from "axios";
function App() {
  const [password, setPassword] = useState("");
  const [result, setResult] = useState("");

  const analyzePassword = async () => {
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/analyze",
        {
          password: password,
        }
      );

      setResult(response.data.strength);
    } catch (error) {
      console.log(error);
      setResult("Backend Connection Error");
    }
  };

  return (
    <div className="container">
      <h1>Adaptive Credential Intelligence</h1>

      <input
        type="password"
        placeholder="Enter Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <button onClick={analyzePassword}>
        Analyze Password
      </button>

      <h2>{result}</h2>
    </div>
  );
}

export default App;