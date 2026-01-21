from app import mongo
from bson import ObjectId
from datetime import datetime

def crear_observacion(data):
    observacion = {
        "riesgo_id": ObjectId(data["riesgo_id"]),
        "tipo": data["tipo"],
        "comentario": data["comentario"],
        "autor": data["autor"],
        "fecha": datetime.now()
    }

    mongo.db.observaciones.insert_one(observacion)
    observacion["_id"] = str(observacion["_id"])
    return observacion
