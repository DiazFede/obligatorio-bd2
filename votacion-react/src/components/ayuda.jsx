import { useNavigate } from "react-router-dom";
import "../styles/ayuda.css";

export default function Ayuda() {
    const navigate = useNavigate();

    return (
        <div className="ayuda-container">
            <h1 className="ayuda-title">Ayuda - Sistema de Votación Online</h1>

            <section className="ayuda-section">
                <h2>¿Cómo sé mi número de credencial?</h2>
                <p>
                    Para obtener tu número de credencial cívica en Uruguay, debes tramitarla en la Corte Electoral, presentando tu partida de nacimiento y cédula de identidad en la oficina correspondiente a tu departamento. Una vez realizada la inscripción, se te asignará una credencial cívica con un número único que identifica tu registro de votante en el padrón electoral uruguayo. Puedes consultar tu número de credencial en la página oficial de la Corte Electoral o en su app de consulta de padrón.
                </p>
            </section>

            <section className="ayuda-section">
                <h2>¿Cómo participo en una elección?</h2>
                <p>
                    Para participar en una elección a través de este sistema de votación online, primero debes iniciar sesión con tu número de credencial y cédula. Luego, se te mostrará el número de circuito al que perteneces y las elecciones disponibles en las que puedes votar. Al presionar "Participar", podrás visualizar las listas u opciones disponibles y emitir tu voto de forma anónima y segura. Tras emitir tu voto, la elección desaparecerá de tu lista de disponibles para garantizar que cada ciudadano vote una única vez por elección.
                </p>
            </section>

            <div className="ayuda-button-container">
                <button
                    className="ayuda-button"
                    onClick={() => navigate("/")}
                >
                    Volver al inicio
                </button>
            </div>
        </div>
    );
}