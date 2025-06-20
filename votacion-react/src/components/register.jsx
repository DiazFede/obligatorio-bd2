import { useState } from "react";
import axios from "axios";

export default function Register() {
  const [formData, setFormData] = useState({
    numero_credencial: "",
    CI: "",
    nombre: "",
    apellido: "",
    edad: ""
  });
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  function handleChange(e) {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setSuccess(null);
    try {
      await axios.post("http://localhost:5000/auth/registrar", formData);
      setSuccess("Registro exitoso. Ya podés iniciar sesión.");
      setFormData({
        numero_credencial: "",
        CI: "",
        nombre: "",
        apellido: "",
        edad: ""
      });
    } catch (err) {
      console.error(err);
      setError("Error al registrar, revisá los datos o intenta más tarde.");
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        name="numero_credencial"
        value={formData.numero_credencial}
        onChange={handleChange}
        placeholder="Número de credencial"
        required
      />
      <input
        name="CI"
        value={formData.CI}
        onChange={handleChange}
        placeholder="Cédula de identidad"
        required
      />
      <input
        name="nombre"
        value={formData.nombre}
        onChange={handleChange}
        placeholder="Nombre"
        required
      />
      <input
        name="apellido"
        value={formData.apellido}
        onChange={handleChange}
        placeholder="Apellido"
        required
      />
      <input
        name="edad"
        type="number"
        min="18"
        value={formData.edad}
        onChange={handleChange}
        placeholder="Edad"
        required
      />
      <button type="submit">Registrar</button>
      {error && <p style={{color: "red"}}>{error}</p>}
      {success && <p style={{color: "green"}}>{success}</p>}
    </form>
  );
}
