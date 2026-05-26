import { useData } from "./useData.js";
import { api } from "../api.js";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, Legend,
  LineChart, Line, CartesianGrid, ResponsiveContainer,
} from "recharts";

export default function TicketsSection() {
  const estado = useData(api.tickets.porEstado);
  const topico = useData(api.tickets.porTopico);
  const tendencia = useData(api.tickets.tendenciaMensual);
  const criticos = useData(api.tickets.topicosCriticos);
  const empleado = useData(api.tickets.porEmpleado);

  return (
    <div className="gap-16">
      <h2 className="section-title">Tickets</h2>

      <div className="grid-2">
        <div className="card">
          <div className="card-title">Por Estado</div>
          {estado.loading ? <div className="loading">...</div> : (
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={estado.data} layout="vertical">
                <XAxis type="number" />
                <YAxis type="category" dataKey="estado" width={90} tick={{ fontSize: 12 }} />
                <Tooltip />
                <Bar dataKey="total" fill="#007B99" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>

        <div className="card">
          <div className="card-title">Tópicos Críticos (abiertos)</div>
          {criticos.loading ? <div className="loading">...</div> : (
            <ResponsiveContainer width="100%" height={220}>
              <BarChart data={criticos.data} layout="vertical">
                <XAxis type="number" />
                <YAxis type="category" dataKey="topico" width={120} tick={{ fontSize: 11 }} />
                <Tooltip />
                <Bar dataKey="tickets_abiertos" fill="#F39200" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>

      <div className="card">
        <div className="card-title">Tendencia Mensual</div>
        {tendencia.loading ? <div className="loading">...</div> : (
          <ResponsiveContainer width="100%" height={240}>
            <LineChart data={tendencia.data}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="mes_creacion" tick={{ fontSize: 11 }} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="total" stroke="#007B99" strokeWidth={2} dot={false} name="Total" />
              <Line type="monotone" dataKey="abiertos" stroke="#F39200" strokeWidth={2} dot={false} name="Abiertos" />
              <Line type="monotone" dataKey="cerrados" stroke="#848585" strokeWidth={2} dot={false} name="Cerrados" />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>

      <div className="card">
        <div className="card-title">Por Tópico</div>
        {topico.loading ? <div className="loading">...</div> : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Tópico</th>
                  <th>Total</th>
                  <th>Abiertos</th>
                  <th>Cerrados</th>
                </tr>
              </thead>
              <tbody>
                {topico.data?.map((row) => (
                  <tr key={row.topico}>
                    <td>{row.topico}</td>
                    <td>{row.total}</td>
                    <td style={{ color: "#dc3545", fontWeight: 600 }}>{row.abiertos}</td>
                    <td style={{ color: "#28a745" }}>{row.cerrados}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div className="card">
        <div className="card-title">Por Empleado</div>
        {empleado.loading ? <div className="loading">...</div> : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Empleado</th>
                  <th>Total</th>
                  <th>Abiertos</th>
                  <th>Cerrados</th>
                </tr>
              </thead>
              <tbody>
                {empleado.data?.slice(0, 20).map((row) => (
                  <tr key={row.empleado}>
                    <td>{row.empleado}</td>
                    <td>{row.total}</td>
                    <td style={{ color: "#dc3545" }}>{row.abiertos}</td>
                    <td style={{ color: "#28a745" }}>{row.cerrados}</td>
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
