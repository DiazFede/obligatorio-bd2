import { useState } from "react";
import axios from "axios";
import { saveToken } from "../utils/auth";
import { useNavigate, Link } from "react-router-dom";

export default function Login() {
  const [credencial, setCredencial] = useState("");
  const [ci, setCi] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    try {
      const res = await axios.post("http://localhost:5000/auth/login", {
        numero_credencial: credencial,
        CI: ci
      });
      saveToken(res.data.access_token);
      navigate("/dashboard");
    } catch {
      setError("Credenciales inválidas");
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-600 to-blue-900 p-6">
      <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-3xl font-bold mb-6 text-center text-blue-800">
          Sistema de Votación - Uruguay
        </h1>
        <form onSubmit={handleSubmit} className="space-y-6">
          <input
            type="text"
            value={credencial}
            onChange={(e) => setCredencial(e.target.value)}
            placeholder="Número de credencial"
            required
            className="w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <input
            type="text"
            value={ci}
            onChange={(e) => setCi(e.target.value)}
            placeholder="Cédula de identidad"
            required
            className="w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            className="w-full bg-blue-700 text-white font-semibold py-3 rounded-md hover:bg-blue-800 transition"
          >
            Ingresar
          </button>
        </form>
        {error && <p className="mt-4 text-center text-red-600 font-medium">{error}</p>}
        <p className="mt-6 text-center text-gray-600">
          ¿No tienes cuenta?{" "}
          <Link to="/register" className="text-blue-700 font-semibold hover:underline">
            Regístrate aquí
          </Link>
        </p>
      </div>
    </div>
  );
}
