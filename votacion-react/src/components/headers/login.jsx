import { useNavigate } from "react-router-dom";
import "../../styles/headers/login.css";

export default function LoginHeader() {
  const navigate = useNavigate();

  return (
    <header className="login-header">
      <button
        className="header-button"
        onClick={() => navigate("/admin-login")}
        aria-label="Administración"
      >
        <i className="fa-solid fa-screwdriver-wrench"></i>
      </button>

      <h1 className="header-title">
        Corte Electoral - Sistema de Votación Online
      </h1>

      <button
        className="header-button"
        onClick={() => navigate("/ayuda")}
        aria-label="Ayuda"
      >
        <i className="fa-solid fa-circle-info"></i>
      </button>
    </header>
  );
}
