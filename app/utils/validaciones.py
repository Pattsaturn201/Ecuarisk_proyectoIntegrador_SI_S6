def validar_activo(data):
    errores = []

    if "nombre" not in data or not isinstance(data["nombre"], str):
        errores.append("El nombre del activo es obligatorio")

    if data.get("tipo") not in ["Hardware", "Software", "Datos", "Personas", "Procesos", "Servicios"]:
        errores.append("Tipo de activo inválido")

    for campo in ["confidencialidad", "integridad", "disponibilidad"]:
        if campo not in data or not isinstance(data[campo], int) or not (1 <= data[campo] <= 4):
            errores.append(f"{campo} debe ser un entero entre 1 y 4")

    if "estado" in data and data["estado"] not in ["Activo", "Inactivo"]:
        errores.append("Estado inválido")

    if "datos_personales" in data:
        if not isinstance(data["datos_personales"].get("procesa"), bool):
            errores.append("datos_personales.procesa debe ser boolean")

    return errores

def validar_riesgo(data):
    errores = []

    if "activo_id" not in data:
        errores.append("activo_id es obligatorio")

    for campo in ["impacto", "probabilidad"]:
        if campo not in data or not isinstance(data[campo], int) or not (1 <= data[campo] <= 4):
            errores.append(f"{campo} debe estar entre 1 y 4")

    if not data.get("amenaza"):
        errores.append("La amenaza es obligatoria")

    return errores

def validar_tratamiento(data):
    errores = []

    if "riesgo_id" not in data:
        errores.append("riesgo_id es obligatorio")

    if data.get("estrategia") not in ["Mitigar", "Transferir", "Aceptar", "Evitar"]:
        errores.append("Estrategia inválida")

    if "responsable" not in data or not isinstance(data["responsable"], str):
        errores.append("Responsable obligatorio")

    if data["estrategia"] == "Mitigar" and not data.get("controles_propuestos"):
        errores.append("Mitigar requiere controles propuestos")

    if data["estrategia"] == "Aceptar" and data.get("controles_propuestos"):
        errores.append("Aceptar no debe tener controles")

    return errores



