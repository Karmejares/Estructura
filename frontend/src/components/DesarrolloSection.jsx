import { useData } from "./useData.js";
import { api } from "../api.js";
import {
  PieChart, Pie, Cell, Tooltip, Legend,
  LineChart, Line, XAxis, YAxis, CartesianGrid, ResponsiveContainer,
} from "recharts";

const ESTADO_COLORS = ["#007B99", "#F39200", "#005f77", "#ffc107", "#848585", "#dc3545"];

export default function DesarrolloSection() {
  const porEstado = useData(api.desarrollo.actividadesPorEstado);
  const cuellos = useData(api.desarrollo.cuellosDeBotella);
  const ciclo = useData(api.desarrollo.cicloPorAsignado);
  const tendencia = useData(api.desarrollo.tendenciaMensual);

  return (
    <div className="gap-16">
      <h2 className="section-title">Desarrollo</h2>

      <div className="grid-2">
        <div className="card">
          <div className="card-title">Actividades por Estado</div>
          {porEstado.loading ? <div className="loading">...</div> : (
            <ResponsiveContainer width="100%" height={220}>
              <PieChart>
                <Pie data={porEstado.data} dataKey="total" nameKey="estado" outerRadius={80} label>
                  {porEstado.data?.map((_, i) => (
                    <Cell key={i} fill={ESTADO_COLORS[i % ESTADO_COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          )}
        </div>

        <div className="card">
          <div className="card-title">Tendencia Mensual de Actividades</div>
          {tendencia.loading ? <div className="loading">...</div> : (
            <ResponsiveContainer width="100%" height={220}>
              <LineChart data={tendencia.data}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="mes_creacion" tick={{ fontSize: 11 }} />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="items_creados" stroke="#007B99" strokeWidth={2} dot={false} name="Creados" />
              </LineChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>

      <div className="card">
        <div className="card-title" style={{ color: "#dc3545" }}>
          Cuellos de Botella — Actividades Retrasadas ({cuellos.data?.length || 0})
        </div>
        {cuellos.loading ? <div className="loading">...</div> : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>#</th>
                  <th>Tipo</th>
                  <th>Título</th>
                  <th>Asignado a</th>
                  <th>Estado</th>
                  <th>Fecha estimada</th>
                  <th>Fecha real</th>
                  <th>Días retraso</th>
                </tr>
              </thead>
              <tbody>
                {cuellos.data?.map((row) => (
                  <tr key={row.id}>
                    <td style={{ fontSize: 11, color: "#888" }}>{row.id}</td>
                    <td>{row.tipo}</td>
                    <td style={{ maxWidth: 280, fontSize: 12 }}>{row.titulo}</td>
                    <td style={{ fontSize: 12 }}>{row.asignado_a}</td>
                    <td>{row.estado}</td>
                    <td>{row.fecha_estimada_cierre}</td>
                    <td>{row.fecha_real_cierre}</td>
                    <td style={{ fontWeight: 700, color: "#dc3545" }}>{row.dias_retraso}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div className="card">
        <div className="card-title">Ciclo por Asignado</div>
        {ciclo.loading ? <div className="loading">...</div> : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Asignado a</th>
                  <th>Items completados</th>
                  <th>Promedio días ciclo</th>
                  <th>Items retrasados</th>
                </tr>
              </thead>
              <tbody>
                {ciclo.data?.map((row) => (
                  <tr key={row.asignado_a}>
                    <td>{row.asignado_a}</td>
                    <td>{row.items_completados}</td>
                    <td>{row.promedio_dias_ciclo}</td>
                    <td style={{ color: row.items_retrasados > 0 ? "#dc3545" : "inherit", fontWeight: row.items_retrasados > 0 ? 700 : 400 }}>
                      {row.items_retrasados}
                    </td>
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
