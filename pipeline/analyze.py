"""Answer strategic infrastructure questions using transformed DataFrames."""

import pandas as pd


# ── TICKETS ──────────────────────────────────────────────────────────────────

def tickets_por_estado(tickets: pd.DataFrame) -> pd.DataFrame:
    result = tickets.groupby("estado").agg(total=("ticket_id", "count")).reset_index()
    return result.sort_values("total", ascending=False)


def tickets_por_topico(tickets: pd.DataFrame) -> pd.DataFrame:
    result = (
        tickets.groupby("topico")
        .agg(
            total=("ticket_id", "count"),
            abiertos=("abierto", "sum"),
            cerrados=("abierto", lambda x: (~x).sum()),
        )
        .reset_index()
    )
    return result.sort_values("total", ascending=False)


def tickets_por_empleado(tickets: pd.DataFrame) -> pd.DataFrame:
    result = (
        tickets.groupby("empleado")
        .agg(
            total=("ticket_id", "count"),
            abiertos=("abierto", "sum"),
            cerrados=("abierto", lambda x: (~x).sum()),
        )
        .reset_index()
    )
    return result.sort_values("total", ascending=False)


def tendencia_mensual_tickets(tickets: pd.DataFrame) -> pd.DataFrame:
    result = (
        tickets.groupby("mes_creacion")
        .agg(
            total=("ticket_id", "count"),
            abiertos=("abierto", "sum"),
            cerrados=("abierto", lambda x: (~x).sum()),
        )
        .reset_index()
    )
    return result.sort_values("mes_creacion")


def topicos_criticos(tickets: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Topics with most open tickets - highest demand pressure points."""
    abiertos = tickets[tickets["abierto"]]
    result = (
        abiertos.groupby("topico")
        .agg(tickets_abiertos=("ticket_id", "count"))
        .reset_index()
        .sort_values("tickets_abiertos", ascending=False)
        .head(top_n)
    )
    return result


# ── INDICADORES ──────────────────────────────────────────────────────────────

def resumen_indicadores(indicators: pd.DataFrame) -> pd.DataFrame:
    cols = ["codigo", "indicador", "periodo", "numerador", "denominador", "porcentaje", "semaforo", "responsable"]
    return indicators[cols].sort_values(["indicador", "periodo"])


def indicadores_en_riesgo(indicators: pd.DataFrame) -> pd.DataFrame:
    """Indicators in yellow or red traffic light."""
    risky = indicators[indicators["semaforo"].isin(["Rojo", "Amarillo"])]
    cols = ["codigo", "indicador", "periodo", "porcentaje", "semaforo", "analisis"]
    return risky[cols].sort_values("porcentaje")


def tendencia_indicadores(indicators: pd.DataFrame) -> pd.DataFrame:
    """Value of each indicator across periods for trend analysis."""
    pivot = indicators.pivot_table(
        index=["codigo", "indicador"],
        columns="periodo",
        values="porcentaje",
        aggfunc="first",
    ).reset_index()
    return pivot


# ── SOFTWARE ─────────────────────────────────────────────────────────────────

def licencias_por_vencer(software_education: pd.DataFrame) -> pd.DataFrame:
    prioritized = software_education[
        software_education["alerta_vencimiento"].isin(["Vencido", "Critico (<=30 dias)", "Alerta (<=90 dias)"])
    ]
    cols = [
        "nombre_software", "campus", "facultad_unidad",
        "fecha_vencimiento", "dias_para_vencer", "alerta_vencimiento",
        "proveedor", "contacto", "correo_contacto",
    ]
    return prioritized[cols].sort_values("dias_para_vencer")


def inventario_por_campus(software_education: pd.DataFrame) -> pd.DataFrame:
    return (
        software_education.groupby(["campus", "alerta_vencimiento"])
        .agg(cantidad_software=("nombre_software", "count"))
        .reset_index()
        .sort_values(["campus", "alerta_vencimiento"])
    )


def inventario_por_tipo_licencia(software_education: pd.DataFrame) -> pd.DataFrame:
    return (
        software_education.groupby("tipo_software")
        .agg(cantidad=("nombre_software", "count"))
        .reset_index()
        .sort_values("cantidad", ascending=False)
    )


# ── DESARROLLO ───────────────────────────────────────────────────────────────

def actividades_por_estado(development: pd.DataFrame) -> pd.DataFrame:
    return (
        development.groupby("estado")
        .agg(total=("id", "count"))
        .reset_index()
        .sort_values("total", ascending=False)
    )


def cuellos_de_botella(development: pd.DataFrame) -> pd.DataFrame:
    """Items completed later than estimated."""
    retrasados = development[development["retrasado"] == True].copy()
    cols = ["id", "tipo", "titulo", "asignado_a", "estado", "fecha_estimada_cierre", "fecha_real_cierre", "dias_retraso"]
    return retrasados[cols].sort_values("dias_retraso", ascending=False)


def ciclo_por_asignado(development: pd.DataFrame) -> pd.DataFrame:
    cerrados = development[development["dias_ciclo"].notna()]
    return (
        cerrados.groupby("asignado_a")
        .agg(
            items_completados=("id", "count"),
            promedio_dias_ciclo=("dias_ciclo", "mean"),
            items_retrasados=("retrasado", "sum"),
        )
        .round(2)
        .reset_index()
        .sort_values("items_completados", ascending=False)
    )


def tendencia_mensual_desarrollo(development: pd.DataFrame) -> pd.DataFrame:
    df = development.copy()
    df["mes_creacion"] = df["fecha_creacion"].dt.to_period("M").astype(str)
    return (
        df.groupby("mes_creacion")
        .agg(items_creados=("id", "count"))
        .reset_index()
        .sort_values("mes_creacion")
    )


# ── RESUMEN EJECUTIVO ─────────────────────────────────────────────────────────

def resumen_ejecutivo(tickets: pd.DataFrame, indicators: pd.DataFrame, development: pd.DataFrame) -> pd.DataFrame:
    total_tickets = len(tickets)
    tickets_abiertos = tickets["abierto"].sum()
    tasa_cierre = round((1 - tickets_abiertos / total_tickets) * 100, 1) if total_tickets > 0 else 0

    indicadores_verdes = (indicators["semaforo"] == "Verde").sum()
    indicadores_totales = len(indicators)
    indicadores_riesgo = (indicators["semaforo"].isin(["Rojo", "Amarillo"])).sum()

    dev_total = len(development)
    dev_cerrados = (development["estado"].str.lower() == "closed").sum()
    dev_retrasados = development["retrasado"].sum()

    rows = [
        ("Tickets totales", total_tickets),
        ("Tickets abiertos", int(tickets_abiertos)),
        ("Tickets cerrados", int(total_tickets - tickets_abiertos)),
        ("Tasa de cierre (%)", tasa_cierre),
        ("Indicadores totales", indicadores_totales),
        ("Indicadores en verde", int(indicadores_verdes)),
        ("Indicadores en riesgo", int(indicadores_riesgo)),
        ("Actividades de desarrollo totales", dev_total),
        ("Actividades cerradas", int(dev_cerrados)),
        ("Actividades con retraso", int(dev_retrasados)),
    ]
    return pd.DataFrame(rows, columns=["Metrica", "Valor"])
