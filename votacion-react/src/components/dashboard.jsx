import { useEffect, useState } from "react";
import axios from "axios";
import "../styles/dashboard.css";
import ModalVotacion from "./ModalVotacion";

export default function Dashboard() {
  const [elecciones, setElecciones] = useState([]);
  const [modalVisible, setModalVisible] = useState(false);
  const [seleccionada, setSeleccionada] = useState(null);
  const [listas, setListas] = useState([]);

  useEffect(() => {
    const numeroCredencial = localStorage.getItem("numero_credencial");
    if (!numeroCredencial) {
      alert("No hay sesión activa. Inicie sesión nuevamente.");
      return;
    }

    axios
      .get(`http://localhost:5000/eleccion/${numeroCredencial}`)
      .then((res) => setElecciones(res.data))
      .catch((err) => console.error("Error al cargar elecciones", err));
  }, []);

  const handleParticipar = (eleccion) => {
    setSeleccionada(eleccion);
    let endpoint;

    switch (eleccion.tipo.toLowerCase()) {
      case "presidencial":
        endpoint = "/listas/presidenciales";
        break;
      case "municipal":
        endpoint = "/listas/municipales";
        break;
      case "ballotage":
        endpoint = "/listas/ballotage";
        break;
      case "plebiscito":
      case "referendum":
        endpoint = "/listas/papeletas";
        break;
      default:
        return;
    }

    axios
      .get(`http://localhost:5000${endpoint}`)
      .then((res) => {
        setListas(res.data);
        setModalVisible(true);
      })
      .catch((err) => {
        console.error("Error al cargar listas", err);
        alert("Error al cargar opciones de votación.");
      });
  };

  const votar = (idLista) => {
    const numeroCredencial = localStorage.getItem("numero_credencial");
    if (!numeroCredencial) {
      alert("Debe iniciar sesión para emitir un voto.");
      return;
    }

    axios
      .post("http://localhost:5000/voto", {
        id_lista: idLista,
        numero_credencial: numeroCredencial,
      })
      .then(() => {
        alert("Voto emitido correctamente.");
        setModalVisible(false);
        // Opcional: recargar elecciones disponibles
        setElecciones((prev) =>
          prev.filter((e) => e.id !== seleccionada.id)
        );
      })
      .catch((err) => {
        if (err.response?.status === 403) {
          alert("Ya has votado en esta elección.");
        } else {
          alert("Error al emitir el voto.");
        }
        console.error(err);
      });
  };

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
            <button className="dashboard-ver" onClick={() => handleParticipar(e)}>
              Participar
            </button>
          </div>
        ))}
      </div>

      {modalVisible && (
        <ModalVotacion
          eleccion={seleccionada}
          listas={listas}
          onClose={() => setModalVisible(false)}
          onVotar={votar}
        />
      )}
    </div>
  );
}
