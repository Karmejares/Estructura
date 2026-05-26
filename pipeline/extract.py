"""Load raw data from Excel source files into DataFrames."""

import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent

TICKETS_FILE = DATA_DIR / "tickets (1).xlsx"
INDICATORS_FILE = DATA_DIR / "Indicadores consolidados (1).xlsx"
SOFTWARE_FILE = DATA_DIR / "Inventario Software Institucional - Eduactivo y Operacional (1).xlsx"
DEVELOPMENT_FILE = DATA_DIR / "Reporte de actividades desarrollo 2026-01 (1).xlsx"

INDICATOR_COLUMNS = [
    "rsp_id", "area", "codigo", "indicador", "periodo",
    "numerador", "denominador", "valor", "analisis",
    "enlace", "responsable", "tiene_plan_accion",
    "id_plan_accion", "correo", "campo_extra_1", "campo_extra_2",
]


def load_tickets() -> pd.DataFrame:
    return pd.read_excel(TICKETS_FILE, sheet_name="DETALLADO")


def load_indicators() -> pd.DataFrame:
    return pd.read_excel(
        INDICATORS_FILE,
        sheet_name="CONSOLIDADO INDICADORES ",
        header=None,
        skiprows=1,
        names=INDICATOR_COLUMNS,
    )


def load_software_education() -> pd.DataFrame:
    return pd.read_excel(SOFTWARE_FILE, sheet_name="SOTWARE EDUCACION", usecols=range(14))


def load_software_operational() -> pd.DataFrame:
    df = pd.read_excel(SOFTWARE_FILE, sheet_name="SOTWARE OPERACIONAL", usecols=range(13))
    return df.dropna(subset=df.columns[1])


def load_development_activities() -> pd.DataFrame:
    return pd.read_excel(DEVELOPMENT_FILE, sheet_name="Reporte de actividades desarrol")
