import { useState } from "react";
import axios from "axios";
import { saveToken } from "../utils/auth";
import { useNavigate, Link } from "react-router-dom";
import LoginHeader from "../components/headers/login";
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
    localStorage.setItem("numero_credencial", res.data.numero_credencial);
    navigate("/dashboard");
  } catch {
    setError("Credenciales inválidas");
  }
}

  return (
    <>
      <LoginHeader />
      <p className="login-text">Bienvenido al sistema de votación online de la Corte Electoral</p>
      <div className="login-container">
        <div className="login-box">
          <h1 className="login-title">
            Iniciar sesion
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
        </div>
      </div>  
    </>
  );
}
