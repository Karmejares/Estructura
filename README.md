# Dashboard TIC — Universidad Católica Luis Amigó

Pipeline ETL + dashboard web para análisis de infraestructura TIC.

## Requisitos

- Python 3.10+
- Node.js 18+

## Instalación

### Python

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Node

```powershell
cd frontend
npm install
```

## Ejecución

Abrir **dos terminales** en la raíz del proyecto.

### Terminal 1 — API (FastAPI)

```powershell
.venv\Scripts\Activate.ps1
uvicorn api.main:app --reload
```

Corre en `http://localhost:8000`

### Terminal 2 — Frontend (React)

```powershell
cd frontend
npm run dev
```

Corre en `http://localhost:5173`

Abrir `http://localhost:5173` en el navegador.

## Uso

| Acción | Descripción |
|---|---|
| **Ejecutar Pipeline** | Recarga los Excel y regenera todos los datos |
| **Descargar Excel** | Descarga `reporte_infraestructura_TIC.xlsx` |
| Tabs en navbar | Resumen · Tickets · Indicadores · Software · Desarrollo |

## Solo pipeline (sin dashboard)

```powershell
.venv\Scripts\Activate.ps1
python main.py
```

Genera `reporte_infraestructura_TIC.xlsx` en la raíz.

## Archivos de datos requeridos

Deben estar en la raíz del proyecto:

- `tickets (1).xlsx`
- `Indicadores consolidados (1).xlsx`
- `Inventario Software Institucional - Eduactivo y Operacional (1).xlsx`
- `Reporte de actividades desarrollo 2026-01 (1).xlsx`
