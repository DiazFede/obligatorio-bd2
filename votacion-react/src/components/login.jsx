import { useState } from "react";
import axios from "axios";
import { saveToken } from "../utils/auth";
import { useNavigate, Link } from "react-router-dom";
import "../styles/login.css";

export default function Login() {
  const [credencial, setCredencial] = useState("");
  const [ci, setCi] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    try {
      const res = await axios.post("http://localhost:5000/auth/login", {
        numero_credencial: credencial,
        CI: ci
      });
      saveToken(res.data.access_token);
      navigate("/dashboard");
    } catch {
      setError("Credenciales inválidas");
    }
  }

  return (
    <div className="login-container">
      <div className="login-box">
        <h1 className="login-title">
          Sistema de Votación - Uruguay
        </h1>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={credencial}
            onChange={(e) => setCredencial(e.target.value)}
            placeholder="Credencial"
            required
            className="login-input"
          />
          <input
            type="text"
            value={ci}
            onChange={(e) => setCi(e.target.value)}
            placeholder="CI"
            required
            className="login-input"
          />
          <button type="submit" className="login-button">
            Ingresar
          </button>
        </form>
        {error && <p className="login-error">{error}</p>}
        <p className="login-footer">
          ¿No tienes cuenta?{" "}
          <Link to="/register">Regístrate aquí</Link>
        </p> 
      </div>
    </div>
  );
}
