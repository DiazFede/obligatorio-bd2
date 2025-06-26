import "../styles/modal.css";

export default function ModalVotacion({ eleccion, listas, onClose, onVotar }) {
  if (!eleccion) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2>{eleccion.tipo} - {eleccion.fecha}</h2>
        <div className="listas-container">
          {listas.map((lista) => (
            <div key={lista.id} className="lista-card">
              <p><strong>ID:</strong> {lista.id}</p>
              {eleccion.tipo === "Presidencial" && (
                <>
                  <p><strong>Presidente:</strong> {lista.presidente}</p>
                  <p><strong>Vicepresidente:</strong> {lista.vicepresidente}</p>
                  <p><strong>Senadores:</strong> {lista.senadores}</p>
                  <p><strong>Diputados:</strong> {lista.diputados}</p>
                </>
              )}
              {eleccion.tipo === "Municipal" || eleccion.tipo === "Ballotage" ? (
                <p><strong>Candidato:</strong> {lista.candidato}</p>
              ) : null}
              {eleccion.tipo === "Plebiscito" || eleccion.tipo === "Referendum" ? (
                <p><strong>Opción:</strong> {lista.opcion}</p>
              ) : null}
              <button onClick={() => onVotar(lista.id)}>Votar</button>
            </div>
          ))}
        </div>
        <button onClick={onClose}>Cerrar</button>
      </div>
    </div>
  );
}