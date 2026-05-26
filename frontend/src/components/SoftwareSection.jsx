import { useData } from "./useData.js";
import { api } from "../api.js";
import { PieChart, Pie, Cell, Tooltip, Legend, BarChart, Bar, XAxis, YAxis, ResponsiveContainer } from "recharts";

const ALERTA_CLASS = {
  "Vencido": "badge-vencido",
  "Critico (<=30 dias)": "badge-critico",
  "Alerta (<=90 dias)": "badge-alerta",
  "Vigente": "badge-vigente",
  "Sin fecha": "badge-gris",
};

const ALERTA_COLORS = {
  "Vencido": "#dc3545",
  "Critico (<=30 dias)": "#fd7e14",
  "Alerta (<=90 dias)": "#ffc107",
  "Vigente": "#28a745",
  "Sin fecha": "#adb5bd",
};

function AlertaBadge({ value }) {
  return <span className={`badge ${ALERTA_CLASS[value] || "badge-gris"}`}>{value}</span>;
}

export default function SoftwareSection() {
  const licencias = useData(api.software.licenciasPorVencer);
  const porTipo = useData(api.software.inventarioPorTipo);
  const porCampus = useData(api.software.inventarioPorCampus);

  return (
    <div className="gap-16">
      <h2 className="section-title">Software & Licencias</h2>

      <div className="grid-2">
        <div className="card">
          <div className="card-title">Inventario por Tipo de Licencia</div>
          {porTipo.loading ? <div className="loading">...</div> : (
            <ResponsiveContainer width="100%" height={220}>
              <PieChart>
                <Pie data={porTipo.data} dataKey="cantidad" nameKey="tipo_software" outerRadius={80} label>
                  {porTipo.data?.map((_, i) => (
                    <Cell key={i} fill={["#007B99","#F39200","#005f77","#ffc107","#848585","#dc3545"][i % 6]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          )}
        </div>

        <div className="card">
          <div className="card-title">Inventario por Campus</div>
          {porCampus.loading ? <div className="loading">...</div> : (
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={
                Object.values(
                  (porCampus.data || []).reduce((acc, row) => {
                    if (!acc[row.campus]) acc[row.campus] = { campus: row.campus };
                    acc[row.campus][row.alerta_vencimiento] = row.cantidad_software;
                    return acc;
                  }, {})
                )
              }>
                <XAxis dataKey="campus" tick={{ fontSize: 11 }} />
                <YAxis />
                <Tooltip />
                <Legend />
                {Object.keys(ALERTA_COLORS).map((key) => (
                  <Bar key={key} dataKey={key} stackId="a" fill={ALERTA_COLORS[key]} />
                ))}
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>

      <div className="card">
        <div className="card-title" style={{ color: "#dc3545" }}>
          Licencias en Alerta ({licencias.data?.length || 0})
        </div>
        {licencias.loading ? <div className="loading">...</div> : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Software</th>
                  <th>Campus</th>
                  <th>Facultad / Unidad</th>
                  <th>Vencimiento</th>
                  <th>Días</th>
                  <th>Alerta</th>
                  <th>Proveedor</th>
                  <th>Contacto</th>
                </tr>
              </thead>
              <tbody>
                {licencias.data?.map((row, i) => (
                  <tr key={i}>
                    <td style={{ fontWeight: 600 }}>{row.nombre_software}</td>
                    <td>{row.campus}</td>
                    <td style={{ fontSize: 12 }}>{row.facultad_unidad}</td>
                    <td>{row.fecha_vencimiento}</td>
                    <td style={{ fontWeight: 700, color: row.dias_para_vencer < 0 ? "#dc3545" : "#fd7e14" }}>
                      {row.dias_para_vencer}
                    </td>
                    <td><AlertaBadge value={row.alerta_vencimiento} /></td>
                    <td style={{ fontSize: 12 }}>{row.proveedor}</td>
                    <td style={{ fontSize: 12 }}>{row.contacto}</td>
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
