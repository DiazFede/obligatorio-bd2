import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
ChartJS.register(ArcElement, Tooltip, Legend);

export default function ResultadosChart({ resultados }) {
  const data = {
    labels: resultados.map((r) => `${r.candidato} (${r.id_lista})`),
    datasets: [
      {
        label: "Votos",
        data: resultados.map((r) => r.votos),
        backgroundColor: [
          "#003366",
          "#3366cc",
          "#99ccff",
          "#6699cc",
          "#004080",
          "#66cccc",
          "#3399cc",
          "#cce6ff",
          "#99ccff",
        ],
        borderColor: "#ffffff",
        borderWidth: 2,
      },
    ],
  };

  return (
    <div style={{ maxWidth: "400px", margin: "0 auto" }}>
      <Pie data={data} />
    </div>
  );
}