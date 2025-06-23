import { useEffect, useState } from "react";
import axios from "axios";
import "../styles/dashboard.css";

export default function Dashboard() {
  const [elecciones, setElecciones] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:5000/eleccion")
      .then((res) => setElecciones(res.data))
      .catch((err) => console.error("Error al cargar elecciones", err));
  }, []);

  return (
    <div className="dashboard-container">
      <h1 className="dashboard-title">Elecciones disponibles</h1>
      <div className="dashboard-list">
        {elecciones.map((e) => (
          <div key={e.id} className="dashboard-item">
            <div className="dashboard-info">
              <p className="dashboard-tipo">{e.tipo}</p>
              <p className="dashboard-fecha">{e.fecha}</p>
            </div>
            <button className="dashboard-ver">Participar</button>
          </div>
        ))}
      </div>
    </div>
  );
}