import { useData } from "./useData.js";
import { api } from "../api.js";

function SemaforoBadge({ value }) {
  const map = {
    Verde: "badge-verde",
    Amarillo: "badge-amarillo",
    Rojo: "badge-rojo",
    Gris: "badge-gris",
  };
  return <span className={`badge ${map[value] || "badge-gris"}`}>{value}</span>;
}

export default function IndicadoresSection() {
  const resumen = useData(api.indicadores.resumen);
  const enRiesgo = useData(api.indicadores.enRiesgo);

  return (
    <div className="gap-16">
      <h2 className="section-title">Indicadores</h2>

      {enRiesgo.data?.length > 0 && (
        <div className="card" style={{ borderLeft: "4px solid #dc3545" }}>
          <div className="card-title" style={{ color: "#dc3545" }}>
            Indicadores en Riesgo ({enRiesgo.data.length})
          </div>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 12 }}>
            {enRiesgo.data?.map((row) => (
              <div
                key={row.codigo + row.periodo}
                style={{
                  background: "#fff5f5",
                  border: "1px solid #f5c6cb",
                  borderRadius: 8,
                  padding: "12px 16px",
                  minWidth: 220,
                  flex: "1 1 220px",
                }}
              >
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
                  <span style={{ fontSize: 11, color: "#888" }}>{row.codigo} · {row.periodo}</span>
                  <SemaforoBadge value={row.semaforo} />
                </div>
                <div style={{ fontWeight: 600, fontSize: 13 }}>{row.indicador}</div>
                <div style={{ fontSize: 20, fontWeight: 800, color: row.semaforo === "Rojo" ? "#dc3545" : "#856404", marginTop: 4 }}>
                  {row.porcentaje}%
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="card">
        <div className="card-title">Todos los Indicadores</div>
        {resumen.loading ? <div className="loading">...</div> : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Código</th>
                  <th>Indicador</th>
                  <th>Periodo</th>
                  <th>Numerador</th>
                  <th>Denominador</th>
                  <th>%</th>
                  <th>Estado</th>
                  <th>Responsable</th>
                </tr>
              </thead>
              <tbody>
                {resumen.data?.map((row) => (
                  <tr key={row.codigo + row.periodo}>
                    <td><code style={{ fontSize: 11 }}>{row.codigo}</code></td>
                    <td>{row.indicador}</td>
                    <td>{row.periodo}</td>
                    <td>{row.numerador}</td>
                    <td>{row.denominador}</td>
                    <td style={{ fontWeight: 700 }}>{row.porcentaje}%</td>
                    <td><SemaforoBadge value={row.semaforo} /></td>
                    <td style={{ fontSize: 12 }}>{row.responsable}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
