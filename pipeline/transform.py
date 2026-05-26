"""Clean and enrich raw DataFrames, computing derived fields."""

import re
import pandas as pd
from datetime import datetime

TODAY = datetime.today()


def _parse_spanish_datetime(value: str) -> pd.Timestamp | None:
    if not isinstance(value, str):
        return None
    normalized = value.strip().replace("a. m.", "AM").replace("p. m.", "PM")
    try:
        return pd.to_datetime(normalized, format="%d/%m/%Y %I:%M:%S %p")
    except Exception:
        return None


def transform_tickets(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()
    df.columns = [
        "tipo", "ticket_id", "fecha_creacion", "cedula",
        "usuario", "asunto", "estado", "topico", "empleado", "cuerpo",
    ]
    df["fecha_creacion"] = pd.to_datetime(df["fecha_creacion"], errors="coerce")
    df["mes_creacion"] = df["fecha_creacion"].dt.to_period("M").astype(str)
    df["estado"] = df["estado"].str.strip()
    df["topico"] = df["topico"].str.strip()
    df["empleado"] = df["empleado"].str.strip()
    df["abierto"] = df["estado"].str.lower() != "cerrar"
    return df


def transform_indicators(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()
    df = df.dropna(subset=["indicador"])
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    df["numerador"] = pd.to_numeric(df["numerador"], errors="coerce")
    df["denominador"] = pd.to_numeric(df["denominador"], errors="coerce")
    df["porcentaje"] = (df["valor"] * 100).round(2)
    df["periodo"] = df["periodo"].astype(str).str.strip()

    # Infer traffic light: extract target from analysis text (heuristic)
    def semaforo(row: pd.Series) -> str:
        valor = row["valor"]
        if pd.isna(valor):
            return "Gris"
        if valor >= 0.95:
            return "Verde"
        if valor >= 0.80:
            return "Amarillo"
        return "Rojo"

    df["semaforo"] = df.apply(semaforo, axis=1)
    return df


def transform_software_education(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()
    df.columns = [
        "tipo_software", "nombre_software", "cantidad_licencias",
        "fecha_vencimiento", "fecha_verificacion", "tipo_licencia",
        "proveedor", "contacto", "correo_contacto", "evidencia",
        "campus", "facultad_unidad", "ubicacion", "observaciones",
    ]
    df = df.dropna(subset=["nombre_software"])
    df["fecha_vencimiento"] = pd.to_datetime(df["fecha_vencimiento"], errors="coerce")
    df["dias_para_vencer"] = (df["fecha_vencimiento"] - TODAY).dt.days
    df["alerta_vencimiento"] = df["dias_para_vencer"].apply(_classify_expiry)
    return df


def transform_software_operational(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()
    df.columns = [
        "tipo_software", "nombre_software", "cantidad_licencias",
        "fecha_vencimiento", "fecha_verificacion", "tipo_licencia",
        "proveedor", "contacto", "correo_contacto", "evidencia",
        "campus", "facultad_unidad", "ubicacion",
    ]
    df["fecha_vencimiento"] = pd.to_datetime(df["fecha_vencimiento"], errors="coerce")
    df["dias_para_vencer"] = (df["fecha_vencimiento"] - TODAY).dt.days
    df["alerta_vencimiento"] = df["dias_para_vencer"].apply(_classify_expiry)
    return df


def transform_development(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()
    df.columns = [
        "id", "tipo", "titulo", "asignado_a",
        "estado", "fecha_creacion", "fecha_estimada_cierre", "fecha_real_cierre",
    ]
    for col in ["fecha_creacion", "fecha_estimada_cierre", "fecha_real_cierre"]:
        df[col] = df[col].apply(_parse_spanish_datetime)

    df["asignado_a"] = df["asignado_a"].str.extract(r"^([^<]+)").iloc[:, 0].str.strip()

    df["dias_ciclo"] = (
        (df["fecha_real_cierre"] - df["fecha_creacion"]).dt.total_seconds() / 86400
    ).round(1)

    df["dias_retraso"] = (
        (df["fecha_real_cierre"] - df["fecha_estimada_cierre"]).dt.total_seconds() / 86400
    ).round(1)

    df["retrasado"] = (df["dias_retraso"] > 0) & df["fecha_real_cierre"].notna()
    return df


def _classify_expiry(days: float) -> str:
    if pd.isna(days):
        return "Sin fecha"
    if days < 0:
        return "Vencido"
    if days <= 30:
        return "Critico (<=30 dias)"
    if days <= 90:
        return "Alerta (<=90 dias)"
    return "Vigente"
