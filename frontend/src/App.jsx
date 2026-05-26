import { useState, useEffect } from "react";
import { api } from "./api.js";
import ResumenSection from "./components/ResumenSection.jsx";
import TicketsSection from "./components/TicketsSection.jsx";
import IndicadoresSection from "./components/IndicadoresSection.jsx";
import SoftwareSection from "./components/SoftwareSection.jsx";
import DesarrolloSection from "./components/DesarrolloSection.jsx";

const TABS = [
  { id: "resumen", label: "Resumen Ejecutivo" },
  { id: "tickets", label: "Tickets" },
  { id: "indicadores", label: "Indicadores" },
  { id: "software", label: "Software" },
  { id: "desarrollo", label: "Desarrollo" },
];

export default function App() {
  const [activeTab, setActiveTab] = useState("resumen");
  const [pipelineRunning, setPipelineRunning] = useState(false);
  const [lastUpdate, setLastUpdate] = useState(null);

  async function handleEjecutar() {
    setPipelineRunning(true);
    try {
      await api.ejecutarPipeline();
      setLastUpdate(new Date().toLocaleTimeString("es-CO"));
      setTimeout(() => setPipelineRunning(false), 3000);
    } catch {
      setPipelineRunning(false);
    }
  }

  useEffect(() => {
    setLastUpdate(new Date().toLocaleTimeString("es-CO"));
  }, []);

  return (
    <>
      <nav className="navbar">
        <span className="navbar-brand">TIC · Unicatólica Luis Amigó</span>
        <div className="navbar-tabs">
          {TABS.map((tab) => (
            <button
              key={tab.id}
              className={`navbar-tab ${activeTab === tab.id ? "active" : ""}`}
              onClick={() => setActiveTab(tab.id)}
            >
              {tab.label}
            </button>
          ))}
        </div>
        <div className="navbar-actions">
          {lastUpdate && (
            <span className="status-bar">Actualizado: {lastUpdate}</span>
          )}
          <button
            className="btn btn-outline"
            onClick={() => window.open("/api/pipeline/descargar")}
          >
            Descargar Excel
          </button>
          <button
            className="btn btn-primary"
            onClick={handleEjecutar}
            disabled={pipelineRunning}
          >
            {pipelineRunning ? "Ejecutando..." : "Ejecutar Pipeline"}
          </button>
        </div>
      </nav>

      <main className="page">
        {activeTab === "resumen" && <ResumenSection />}
        {activeTab === "tickets" && <TicketsSection />}
        {activeTab === "indicadores" && <IndicadoresSection />}
        {activeTab === "software" && <SoftwareSection />}
        {activeTab === "desarrollo" && <DesarrolloSection />}
      </main>
    </>
  );
}
