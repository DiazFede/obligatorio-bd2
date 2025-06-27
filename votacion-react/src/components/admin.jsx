import { useEffect, useState } from "react";
import axios from "axios";
import "../styles/admin.css";

export default function Admin() {
  const [elecciones, setElecciones] = useState([]);

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
        status: nuevoEstado
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

  return (
    <div className="admin-container">
      <h1 className="admin-title">Administrar Elecciones</h1>
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
              <td>{e.fecha}</td>
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
    </div>
  );
}
