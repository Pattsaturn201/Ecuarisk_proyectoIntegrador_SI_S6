from app import mongo
from datetime import datetime
from bson import ObjectId
from app.utils.validaciones import validar_activo

def calcular_clasificacion(valor):
    if valor >= 3.5:
        return "Crítico"
    elif valor >= 2.5:
        return "Alto"
    elif valor >= 1.5:
        return "Medio"
    return "Bajo"


def create_activo(data):
    # 1️⃣ Validación
    errores = validar_activo(data)
    if errores:
        return {"errores": errores}, 400

    # 2️⃣ Evitar duplicados
    if mongo.db.activos.find_one({"nombre": data["nombre"]}):
        return {"error": "Ya existe un activo con ese nombre"}, 409

    # 3️⃣ Cálculo CIA
    c = data["confidencialidad"]
    i = data["integridad"]
    d = data["disponibilidad"]
    valor = round((c + i + d) / 3, 2)

    clasificacion = calcular_clasificacion(valor)

    # 4️⃣ Construcción del documento
    activo = {
        "nombre": data["nombre"],
        "tipo": data["tipo"],
        "descripcion": data.get("descripcion"),
        "area": data.get("area"),
        "propietario": data.get("propietario"),
        "ubicacion": data.get("ubicacion"),
        "estado": data.get("estado", "Activo"),
        "fecha_creacion": datetime.now(),
        "valoracion": {
            "confidencialidad": c,
            "integridad": i,
            "disponibilidad": d,
            "valor": valor,
            "clasificacion": clasificacion
        },
        "datos_personales": {
            "procesa": data.get("datos_personales", {}).get("procesa", False),
            "sensibles": data.get("datos_personales", {}).get("sensibles", False),
            "volumen": data.get("datos_personales", {}).get("volumen", "Bajo")
        }
    }

    # 5️⃣ Guardar en MongoDB
    result = mongo.db.activos.insert_one(activo)

    # 6️⃣ Respuesta limpia
    activo["_id"] = str(result.inserted_id)
    return activo
