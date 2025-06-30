import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "../styles/admin.css";

export default function AdminAutorizar() {
  const [numeroCredencial, setNumeroCredencial] = useState("");
  const [idEleccion, setIdEleccion] = useState("");
  const [numeroCircuito, setNumeroCircuito] = useState("");
  const [mensaje, setMensaje] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMensaje("");

    try {
      await axios.post("http://localhost:5000/acto-electoral/autorizar", {
        numero_credencial: numeroCredencial,
        id_eleccion: idEleccion,
        numero_circuito: numeroCircuito
      });
      setMensaje("Ciudadano autorizado correctamente.");
      setNumeroCredencial("");
      setIdEleccion("");
      setNumeroCircuito("");
    } catch (err) {
      if (err.response?.data?.error) {
        setMensaje(err.response.data.error);
      } else {
        setMensaje("Error al autorizar ciudadano.");
      }
    }
  };

  return (
    <div className="admin-container">
      <h1 className="admin-title">Autorizar Ciudadano</h1>
      <form className="admin-form" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Número de credencial"
          value={numeroCredencial}
          onChange={(e) => setNumeroCredencial(e.target.value)}
          required
          className="admin-input"
        />
        <input
          type="number"
          placeholder="ID de elección"
          value={idEleccion}
          onChange={(e) => setIdEleccion(e.target.value)}
          required
          className="admin-input"
        />
        <input
          type="number"
          placeholder="Número de circuito"
          value={numeroCircuito}
          onChange={(e) => setNumeroCircuito(e.target.value)}
          required
          className="admin-input"
        />
        <button type="submit" className="admin-button">
          Autorizar
        </button>
      </form>
      {mensaje && <p style={{ marginTop: "1rem", color: "#003366", textAlign: "center" }}>{mensaje}</p>}
      <div className="logout-container">
        <button className="admin-button logout-button" onClick={() => navigate("/admin")}>
          Volver al panel
        </button>
      </div>
    </div>
  );
}