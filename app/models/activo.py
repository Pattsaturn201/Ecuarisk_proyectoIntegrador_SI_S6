def validar_activo(data):
    campos = [
        "nombre",
        "tipo",
        "confidencialidad",
        "integridad",
        "disponibilidad"
    ]

    for campo in campos:
        if campo not in data:
            raise ValueError(f"Falta el campo obligatorio: {campo}")

    for campo in ["confidencialidad", "integridad", "disponibilidad"]:
        if not 1 <= int(data[campo]) <= 4:
            raise ValueError(f"{campo} debe estar entre 1 y 4")
