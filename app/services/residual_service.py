from app import mongo
from bson import ObjectId

def calcular_residual(data):
    if "riesgo_id" not in data:
        raise ValueError("Falta riesgo_id")
    if "probabilidad_residual" not in data or "impacto_residual" not in data:
        raise ValueError("Faltan valores de probabilidad o impacto residual")

    try:
        riesgo_id = ObjectId(data["riesgo_id"])
    except:
        raise ValueError("ID de riesgo inválido")

    riesgo = mongo.db.riesgos.find_one({"_id": riesgo_id})
    if not riesgo:
        raise ValueError("Riesgo no encontrado")

    prob_res = int(data["probabilidad_residual"])
    imp_res = int(data["impacto_residual"])
    
    if not (1 <= prob_res <= 4) or not (1 <= imp_res <= 4):
         raise ValueError("Probabilidad e impacto deben estar entre 1 y 4")

    riesgo_residual = prob_res * imp_res
    riesgo_inherente = riesgo["riesgo_inherente"]

    # Evitar división por cero si riesgo inherente es 0 (aunque no debería serlo por validación previa)
    if riesgo_inherente > 0:
        reduccion = round(((riesgo_inherente - riesgo_residual) / riesgo_inherente) * 100, 2)
    else:
        reduccion = 0

    nuevo_residual = {
        "riesgo_id": str(riesgo_id),
        "probabilidad_residual": prob_res,
        "impacto_residual": imp_res,
        "riesgo_residual": riesgo_residual,
        "reduccion_porcentaje": reduccion
    }

    mongo.db.Residual.insert_one(nuevo_residual)
    return nuevo_residual

def obtener_residuales():
    cursor = mongo.db.Residual.find()
    residuales = []
    
    # Cache riesgos para enriquecer
    import app.services.riesgo_service as rs
    
    for res in cursor:
        res["_id"] = str(res["_id"])
        riesgo_id = str(res["riesgo_id"])
        
        riesgo = mongo.db.riesgos.find_one({"_id": ObjectId(riesgo_id)})
        
        if riesgo:
             # Obtener info del activo tambien si es posible
            activo = mongo.db.activos.find_one({"_id": riesgo["activo_id"]})
            nombre_activo = activo["nombre"] if activo else "Desconocido"
            
            res["detalle_riesgo"] = f"{riesgo['descripcion']} en {nombre_activo}"
            res["riesgo_inherente"] = riesgo["riesgo_inherente"]
        else:
            res["detalle_riesgo"] = "Riesgo no encontrado"
            res["riesgo_inherente"] = "?"
            
        residuales.append(res)
    
    return residuales
