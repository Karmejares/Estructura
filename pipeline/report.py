"""Generate Excel report with one sheet per analysis."""

import pandas as pd
from pathlib import Path

OUTPUT_FILE = Path(__file__).parent.parent / "reporte_infraestructura_TIC.xlsx"

SHEET_CONFIG = [
    ("Resumen Ejecutivo",       "resumen_ejecutivo"),
    ("Tickets por Estado",      "tickets_por_estado"),
    ("Tickets por Topico",      "tickets_por_topico"),
    ("Tickets por Empleado",    "tickets_por_empleado"),
    ("Tendencia Mensual Tickets", "tendencia_mensual"),
    ("Topicos Criticos",        "topicos_criticos"),
    ("Indicadores",             "resumen_indicadores"),
    ("Indicadores en Riesgo",   "indicadores_en_riesgo"),
    ("Tendencia Indicadores",   "tendencia_indicadores"),
    ("Licencias por Vencer",    "licencias_por_vencer"),
    ("Inv Campus",              "inventario_por_campus"),
    ("Inv Tipo Licencia",       "inventario_por_tipo_licencia"),
    ("Desarrollo por Estado",   "actividades_por_estado"),
    ("Cuellos de Botella",      "cuellos_de_botella"),
    ("Ciclo por Asignado",      "ciclo_por_asignado"),
    ("Tendencia Desarrollo",    "tendencia_desarrollo"),
]

SEMAFORO_COLORS = {
    "Verde":   "#C6EFCE",
    "Amarillo": "#FFEB9C",
    "Rojo":    "#FFC7CE",
    "Gris":    "#D9D9D9",
}

ALERTA_COLORS = {
    "Vencido":              "#FFC7CE",
    "Critico (<=30 dias)":  "#FFEB9C",
    "Alerta (<=90 dias)":   "#FFCC99",
    "Vigente":              "#C6EFCE",
    "Sin fecha":            "#D9D9D9",
}


def _write_sheet(
    writer: pd.ExcelWriter,
    sheet_name: str,
    dataframe: pd.DataFrame,
    color_column: str | None = None,
    color_map: dict | None = None,
) -> None:
    dataframe.to_excel(writer, sheet_name=sheet_name, index=False)
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]

    header_format = workbook.add_format({
        "bold": True,
        "bg_color": "#1F4E79",
        "font_color": "#FFFFFF",
        "border": 1,
        "text_wrap": True,
        "valign": "vcenter",
    })

    for col_num, col_name in enumerate(dataframe.columns):
        worksheet.write(0, col_num, col_name, header_format)
        col_width = max(len(str(col_name)) + 2, 12)
        worksheet.set_column(col_num, col_num, col_width)

    if color_column and color_map and color_column in dataframe.columns:
        color_col_index = dataframe.columns.get_loc(color_column)
        for row_num, value in enumerate(dataframe[color_column], start=1):
            bg = color_map.get(str(value), "#FFFFFF")
            cell_format = workbook.add_format({"bg_color": bg, "border": 1})
            worksheet.write(row_num, color_col_index, value, cell_format)

    worksheet.freeze_panes(1, 0)


def generate_report(analyses: dict[str, pd.DataFrame]) -> Path:
    with pd.ExcelWriter(OUTPUT_FILE, engine="xlsxwriter") as writer:
        mapping = {
            "resumen_ejecutivo":        ("Resumen Ejecutivo",         None,            None),
            "tickets_por_estado":       ("Tickets por Estado",        None,            None),
            "tickets_por_topico":       ("Tickets por Topico",        None,            None),
            "tickets_por_empleado":     ("Tickets por Empleado",      None,            None),
            "tendencia_mensual":        ("Tendencia Mensual Tickets",  None,            None),
            "topicos_criticos":         ("Topicos Criticos",           None,            None),
            "resumen_indicadores":      ("Indicadores",               "semaforo",      SEMAFORO_COLORS),
            "indicadores_en_riesgo":    ("Indicadores en Riesgo",     "semaforo",      SEMAFORO_COLORS),
            "tendencia_indicadores":    ("Tendencia Indicadores",      None,            None),
            "licencias_por_vencer":     ("Licencias por Vencer",      "alerta_vencimiento", ALERTA_COLORS),
            "inventario_por_campus":    ("Inv Campus",                "alerta_vencimiento", ALERTA_COLORS),
            "inventario_por_tipo":      ("Inv Tipo Licencia",          None,            None),
            "actividades_por_estado":   ("Desarrollo por Estado",      None,            None),
            "cuellos_de_botella":       ("Cuellos de Botella",         None,            None),
            "ciclo_por_asignado":       ("Ciclo por Asignado",         None,            None),
            "tendencia_desarrollo":     ("Tendencia Desarrollo",        None,            None),
        }

        for key, (sheet_name, color_col, color_map) in mapping.items():
            if key in analyses and not analyses[key].empty:
                _write_sheet(writer, sheet_name, analyses[key], color_col, color_map)

    return OUTPUT_FILE
