import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import ResultadosChart from "../components/admin/resultadosChart";
import "../styles/admin.css";

export default function Admin() {
  const [elecciones, setElecciones] = useState([]);
  const [eleccionSeleccionada, setEleccionSeleccionada] = useState(null);
  const [resultados, setResultados] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const adminSesion = localStorage.getItem("admin_sesion");
    if (!adminSesion) {
      navigate("/admin-login");
    }
  }, [navigate]);

  useEffect(() => {
    axios
      .get("http://localhost:5000/eleccion/")
      .then((res) => setElecciones(res.data))
      .catch((err) => console.error("Error al cargar elecciones", err));
  }, []);

  const toggleEstado = (id_eleccion, estadoActual) => {
    const nuevoEstado = !estadoActual;

    axios
      .put(`http://localhost:5000/eleccion/${id_eleccion}/status`, {
        status: nuevoEstado,
      })
      .then(() => {
        setElecciones((prev) =>
          prev.map((e) =>
            e.id_eleccion === id_eleccion ? { ...e, status: nuevoEstado } : e
          )
        );
      })
      .catch((err) => {
        console.error("Error al cambiar estado", err);
        alert("Error al cambiar el estado de la elección.");
      });
  };

  const cerrarSesion = () => {
    localStorage.removeItem("admin_sesion");
    navigate("/admin-login");
  };

  const cargarResultados = (id_eleccion) => {
    axios
      .get(`http://localhost:5000/estadisticas/detalle/${id_eleccion}`)
      .then((res) => setResultados(res.data))
      .catch((err) => {
        console.error("Error al cargar resultados", err);
        alert("Error al cargar resultados de la elección.");
      });
  };

  return (
    <div className="admin-container">
      <h1 className="admin-title">Panel de administración</h1>

      <table className="admin-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Tipo</th>
            <th>Fecha</th>
            <th>Estado</th>
            <th>Acción</th>
          </tr>
        </thead>
        <tbody>
          {elecciones.map((e) => (
            <tr key={e.id_eleccion}>
              <td>{e.id_eleccion}</td>
              <td>{e.tipo}</td>
              <td>{new Date(e.fecha).toLocaleDateString("es-ES")}</td>
              <td>{e.status ? "Abierta" : "Cerrada"}</td>
              <td>
                <button
                  className="admin-button"
                  onClick={() => toggleEstado(e.id_eleccion, e.status)}
                >
                  {e.status ? "Cerrar" : "Abrir"}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <div style={{ marginTop: "1rem" }}>
        <label>Seleccionar elección cerrada para ver resultados:</label>
        <select
          className="admin-select"
          onChange={(e) => {
            const id = parseInt(e.target.value);
            setEleccionSeleccionada(id);
            if (id) cargarResultados(id);
            else setResultados([]);
          }}
          value={eleccionSeleccionada || ""}
          style={{ marginLeft: "0.5rem" }}
        >
          <option value="">-- Seleccionar elección --</option>
          {elecciones
            .filter((e) => !e.status)
            .map((e) => (
              <option key={e.id_eleccion} value={e.id_eleccion}>
                {e.tipo} - {new Date(e.fecha).toLocaleDateString("es-ES")}
              </option>
            ))}
        </select>
      </div>

      {resultados.length > 0 && (
        <div style={{ marginTop: "2rem" }}>
          <h2 style={{ textAlign: "center" }}>Resultados de la elección</h2>
          <ResultadosChart resultados={resultados} />
        </div>
      )}

      <div className="logout-container">
        <button
          className="admin-button export-button"
          onClick={() => {
            window.open("http://localhost:5000/estadisticas/exportar", "_blank");
          }}
        >
          Exportar resultados
        </button>
        <button className="admin-button logout-button" onClick={cerrarSesion}>
          Cerrar sesión
        </button>
      </div>
    </div>
  );
}