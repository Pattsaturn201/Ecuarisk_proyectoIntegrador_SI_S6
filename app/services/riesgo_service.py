from app import mongo
from bson import ObjectId

def create_riesgo(data):
    collection = mongo.db.riesgos

    # calculo básico
    nivel = data["impacto"] * data["probabilidad"]

    riesgo = {
        "activo_id": ObjectId(data["activo_id"]),
        "amenaza": data["amenaza"],
        "vulnerabilidad": data["vulnerabilidad"],
        "controles_existentes": data.get("controles_existentes", []),
        "impacto": data["impacto"],
        "probabilidad": data["probabilidad"],
        "nivel": nivel,
        "clasificacion": "Alto" if nivel >= 9 else "Medio"
    }

    result = collection.insert_one(riesgo)
    riesgo["_id"] = str(result.inserted_id)
    return riesgo

def get_riesgos():
    collection = mongo.db.riesgos
    riesgos = list(collection.find())
    for r in riesgos:
        r["_id"] = str(r["_id"])
    return riesgos


    def calcular_riesgo_residual(data):
    impacto = data["impacto_residual"]
    probabilidad = data["probabilidad_residual"]

    nivel = impacto * probabilidad
    clasificacion = clasificar_riesgo(nivel)

    residual = {
        "riesgo_id": ObjectId(data["riesgo_id"]),
        "impacto_residual": impacto,
        "probabilidad_residual": probabilidad,
        "nivel_residual": nivel,
        "clasificacion": clasificacion,
        "fecha_evaluacion": datetime.now()
    }

    mongo.db.riesgo_residual.insert_one(residual)
    residual["_id"] = str(residual["_id"])
    return residual
