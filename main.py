"""Pipeline principal - infraestructura TIC Universidad Católica Luis Amigó."""

from pipeline import extract, transform, analyze, report


def run() -> None:
    print("Extrayendo datos...")
    raw_tickets = extract.load_tickets()
    raw_indicators = extract.load_indicators()
    raw_software_edu = extract.load_software_education()
    raw_software_op = extract.load_software_operational()
    raw_development = extract.load_development_activities()

    print("Transformando datos...")
    tickets = transform.transform_tickets(raw_tickets)
    indicators = transform.transform_indicators(raw_indicators)
    software_edu = transform.transform_software_education(raw_software_edu)
    software_op = transform.transform_software_operational(raw_software_op)
    development = transform.transform_development(raw_development)

    print("Analizando...")
    analyses = {
        "resumen_ejecutivo":     analyze.resumen_ejecutivo(tickets, indicators, development),
        "tickets_por_estado":    analyze.tickets_por_estado(tickets),
        "tickets_por_topico":    analyze.tickets_por_topico(tickets),
        "tickets_por_empleado":  analyze.tickets_por_empleado(tickets),
        "tendencia_mensual":     analyze.tendencia_mensual_tickets(tickets),
        "topicos_criticos":      analyze.topicos_criticos(tickets),
        "resumen_indicadores":   analyze.resumen_indicadores(indicators),
        "indicadores_en_riesgo": analyze.indicadores_en_riesgo(indicators),
        "tendencia_indicadores": analyze.tendencia_indicadores(indicators),
        "licencias_por_vencer":  analyze.licencias_por_vencer(software_edu),
        "inventario_por_campus": analyze.inventario_por_campus(software_edu),
        "inventario_por_tipo":   analyze.inventario_por_tipo_licencia(software_edu),
        "actividades_por_estado": analyze.actividades_por_estado(development),
        "cuellos_de_botella":    analyze.cuellos_de_botella(development),
        "ciclo_por_asignado":    analyze.ciclo_por_asignado(development),
        "tendencia_desarrollo":  analyze.tendencia_mensual_desarrollo(development),
    }

    print("Generando reporte...")
    output_path = report.generate_report(analyses)
    print(f"Reporte generado: {output_path}")

    _print_summary(analyses)


def _print_summary(analyses: dict) -> None:
    print("\n" + "=" * 60)
    print("RESUMEN EJECUTIVO")
    print("=" * 60)
    for _, row in analyses["resumen_ejecutivo"].iterrows():
        print(f"  {row['Metrica']:<40} {row['Valor']}")

    print("\nINDICADORES EN RIESGO:")
    risky = analyses["indicadores_en_riesgo"]
    if risky.empty:
        print("  Ninguno")
    else:
        for _, row in risky.iterrows():
            print(f"  [{row['semaforo']}] {row['indicador']} ({row['periodo']}) - {row['porcentaje']}%")

    print("\nLICENCIAS CRITICAS:")
    criticas = analyses["licencias_por_vencer"]
    if criticas.empty:
        print("  Ninguna")
    else:
        for _, row in criticas.iterrows():
            print(f"  [{row['alerta_vencimiento']}] {row['nombre_software']} - {row['campus']}")

    print("\nCUELLOS DE BOTELLA (desarrollo):")
    cuellos = analyses["cuellos_de_botella"]
    if cuellos.empty:
        print("  Ninguno")
    else:
        for _, row in cuellos.head(5).iterrows():
            print(f"  {row['titulo'][:50]} - {row['dias_retraso']} dias de retraso")


if __name__ == "__main__":
    run()
