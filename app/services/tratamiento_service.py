from app import mongo
from bson import ObjectId
from datetime import datetime
from app.utils.validaciones import validar_tratamiento

def crear_tratamiento(data):
    errores = validar_tratamiento(data)
    if errores:
        return {"errores": errores}, 400

    riesgo = mongo.db.riesgos.find_one({"_id": ObjectId(data["riesgo_id"])})
    if not riesgo:
        return {"error": "Riesgo no encontrado"}, 404

    if riesgo["clasificacion"] not in ["Alto", "Crítico"]:
        return {"error": "El riesgo no requiere tratamiento"}, 400

    tratamiento = {
        "riesgo_id": ObjectId(data["riesgo_id"]),
        "estrategia": data["estrategia"],
        "controles_propuestos": data.get("controles_propuestos", []),
        "responsable": data["responsable"],
        "estado": "Pendiente",
        "fecha_inicio": datetime.now(),
        "fecha_fin": data.get("fecha_fin"),
        "observaciones": data.get("observaciones", "")
    }

    result = mongo.db.tratamientos.insert_one(tratamiento)
    tratamiento["_id"] = str(result.inserted_id)
    tratamiento["riesgo_id"] = str(tratamiento["riesgo_id"])

    return tratamiento

def actualizar_estado_tratamiento(tratamiento_id, estado):
    mongo.db.tratamientos.update_one(
        {"_id": ObjectId(tratamiento_id)},
        {"$set": {"estado": estado}}
    )

