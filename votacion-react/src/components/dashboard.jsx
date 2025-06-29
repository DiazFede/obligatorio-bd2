import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "../styles/dashboard.css";
import ModalVotacion from "./ModalVotacion";

export default function Dashboard() {
  const [elecciones, setElecciones] = useState([]);
  const [modalVisible, setModalVisible] = useState(false);
  const [seleccionada, setSeleccionada] = useState(null);
  const [listas, setListas] = useState([]);
  const [numeroCircuito, setNumeroCircuito] = useState(null);

  const navigate = useNavigate();

  useEffect(() => {
    const numeroCredencial = localStorage.getItem("numero_credencial");
    if (!numeroCredencial) {
      alert("No hay sesión activa. Inicie sesión nuevamente.");
      navigate("/");
      return;
    }

    axios
      .get(`http://localhost:5000/eleccion/${numeroCredencial}`)
      .then((res) => {
        setElecciones(res.data);
        if (res.data.length > 0) {
          setNumeroCircuito(res.data[0].numero_circuito);
        }
      })
      .catch((err) => console.error("Error al cargar elecciones", err));
  }, [navigate]);

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
        id_eleccion: seleccionada.id_eleccion,
      })
      .then(() => {
        alert("Voto emitido correctamente.");
        setModalVisible(false);
        setElecciones((prev) =>
          prev.filter((e) => e.id_eleccion !== seleccionada.id_eleccion)
        );
      })
      .catch((err) => {
        if (err.response?.status === 403) {
          alert(err.response.data.error);
        } else {
          alert("Error al emitir el voto.");
        }
        console.error(err);
      });
  };

  const cerrarSesion = () => {
    localStorage.removeItem("numero_credencial");
    navigate("/");
  };

  return (
    <div className="dashboard-container">
      <h1 className="dashboard-title">Elecciones disponibles</h1>
      {numeroCircuito && (
        <p className="dashboard-fecha">
          Su circuito es el circuito número: {numeroCircuito}
        </p>
      )}
      <div className="dashboard-list">
        {elecciones.map((e) => (
          <div key={e.id_eleccion} className="dashboard-item">
            <div className="dashboard-info">
              <p className="dashboard-tipo">{e.tipo}</p>
              <p className="dashboard-fecha">
                {new Date(e.fecha).toLocaleDateString("es-ES")}
              </p>
            </div>
            <button
              className="dashboard-ver"
              onClick={() => handleParticipar(e)}
            >
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

      <div className="logout-container">
        <button className="admin-button logout-button" onClick={cerrarSesion}>
          Cerrar sesión
        </button>
      </div>
    </div>
  );
}