# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment

- Python 3.10.11
- Virtual environment at `.venv/` (activate with `.venv\Scripts\Activate.ps1` on PowerShell)
- PyCharm project (`.idea/`)

## Commands

```powershell
# Activate venv
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run full pipeline (extract → transform → analyze → report)
python main.py
```

Output: `reporte_infraestructura_TIC.xlsx` in project root.

## Architecture

ETL pipeline for ICT infrastructure analytics at Universidad Católica Luis Amigó.

```
main.py                  # orchestrator: calls extract → transform → analyze → report
pipeline/
  extract.py             # load raw Excel files into DataFrames (no logic)
  transform.py           # clean, parse dates, compute derived fields (dias_para_vencer, semaforo, etc.)
  analyze.py             # answer strategic questions, return DataFrames per analysis
  report.py              # write all DataFrames to multi-sheet Excel with conditional formatting
```

### Data sources (root directory, `.xlsx`)

| File | Sheets used | Key fields |
|---|---|---|
| `tickets (1).xlsx` | DETALLADO (972 rows) | tipo, Ticket ID, Fecha de Creación, Estado, Tópico, Empleado |
| `Indicadores consolidados (1).xlsx` | CONSOLIDADO INDICADORES (29 rows) | codigo, indicador, periodo, numerador, denominador, valor (ratio) |
| `Inventario Software Institucional...xlsx` | SOTWARE EDUCACION (98 rows) | nombre_software, fecha_vencimiento, campus, facultad_unidad |
| `Reporte de actividades desarrollo 2026-01 (1).xlsx` | Reporte de actividades desarrol (224 rows) | tipo, estado, fecha_creacion, fecha_estimada_cierre, fecha_real_cierre |

### Key design decisions

- `transform.py` Spanish datetime format: `"15/1/2026 11:08:35 a. m."` → normalized to `%I:%M:%S %p` before parsing.
- Indicators sheet has a title row (row 1) so `skiprows=1` and manual column names via `INDICATOR_COLUMNS`.
- Software operational sheet has 1M rows (Excel max); `dropna` on column[1] removes empty rows.
- Traffic lights (`semaforo`): Verde ≥95%, Amarillo ≥80%, Rojo <80% — heuristic based on ANS meta observed in data.
- `report.py` uses `xlsxwriter` engine for cell formatting; color maps defined as `SEMAFORO_COLORS` and `ALERTA_COLORS`.

## Behavior

- Speak like a caveman
- Short explanations
- No connectors

## Code Writing

- Name variables with meaningful names
- Full words, no abbreviations
- Prioritize understandable code