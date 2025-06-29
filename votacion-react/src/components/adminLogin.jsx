import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "../styles/login.css";

export default function AdminLogin() {
  const [usuario, setUsuario] = useState("");
  const [contrasena, setContrasena] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    try {
      await axios.post("http://localhost:5000/admin/login", {
        usuario,
        contrasena
      });
      localStorage.setItem("admin_sesion", "true");
      navigate("/admin");
    } catch {
      setError("Credenciales inválidas");
    }
  }

  return (
    <div className="login-container">
      <div className="login-box">
        <h1 className="login-title">Admin - Corte Electoral</h1>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={usuario}
            onChange={(e) => setUsuario(e.target.value)}
            placeholder="Usuario"
            required
            className="login-input"
          />
          <input
            type="password"
            value={contrasena}
            onChange={(e) => setContrasena(e.target.value)}
            placeholder="Contraseña"
            required
            className="login-input"
          />
          <button type="submit" className="login-button">
            Ingresar como Admin
          </button>
        </form>
        {error && <p className="login-error">{error}</p>}
      </div>
    </div>
  );
}
