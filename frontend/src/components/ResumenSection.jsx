import { useData } from "./useData.js";
import { api } from "../api.js";

const KPI_COLORS = {
  "Tasa de cierre (%)":          "#007B99",
  "Indicadores en riesgo":       "#dc3545",
  "Actividades con retraso":     "#F39200",
  "Tickets abiertos":            "#F39200",
  "Indicadores en verde":        "#007B99",
  "Actividades cerradas":        "#007B99",
};

export default function ResumenSection() {
  const { data, loading, error } = useData(api.resumenEjecutivo);

  if (loading) return <div className="loading">Cargando resumen...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="gap-16">
      <h2 className="section-title">Resumen Ejecutivo</h2>
      <div className="grid-4" style={{ gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))" }}>
        {data.map((row) => (
          <div
            key={row.Metrica}
            className="kpi-card"
            style={{ borderLeftColor: KPI_COLORS[row.Metrica] || "#848585" }}
          >
            <div className="kpi-value">{row.Valor}</div>
            <div className="kpi-label">{row.Metrica}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
