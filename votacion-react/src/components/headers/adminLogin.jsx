import { useNavigate } from "react-router-dom";
import "../../styles/headers/login.css";

export default function AdminLoginHeader() {
  const navigate = useNavigate();

  return (
    <header className="login-header">
      <button
        className="header-button"
        onClick={() => navigate("/")}
        title="Volver al inicio"
      >
        <i className="fa-solid fa-house"></i>
      </button>
      <h1 className="login-header-title">Corte Electoral - Administradores</h1>
      <button
        className="header-button invisible-button"
      >
        <i className="fa-solid fa-house"></i>
      </button>
    </header>
  );
}