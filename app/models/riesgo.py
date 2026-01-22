def validar_riesgo(data):
    campos = [
        "activo_id",
        "amenaza",
        "vulnerabilidad",
        "impacto",
        "probabilidad"
    ]

    for campo in campos:
        if campo not in data:
            raise ValueError(f"Falta el campo {campo}")

    if not 1 <= int(data["impacto"]) <= 4:
        raise ValueError("Impacto fuera de rango (1-4)")

    if not 1 <= int(data["probabilidad"]) <= 4:
        raise ValueError("Probabilidad fuera de rango (1-4)")
