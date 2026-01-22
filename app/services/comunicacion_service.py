from app import mongo
from bson import ObjectId
from datetime import datetime

def crear_comunicacion(data):
    required = ["tipo_registro", "descripcion", "responsable"] 
    # tipo_registro: "Observacion", "Recomendacion", "Comentario"
    
    for field in required:
        if field not in data:
            raise ValueError(f"Falta el campo obligatorio: {field}")
            
    # Opcional: vincular a un riesgo o tratamiento si se provee ID
    if "referencia_id" in data and data["referencia_id"]:
         data["referencia_id"] = str(data["referencia_id"]) # Asegurar string

    data["fecha_registro"] = datetime.now().isoformat()
    
    mongo.db.Comunicacion.insert_one(data)
    data["_id"] = str(data["_id"]) # Convertir ObjectId a string para retorno JSON
    return data

def obtener_reporte_completo():
    # Agregación simple para demo, idealmente usar $lookup de mongo
    activos = list(mongo.db.activos.find())
    reporte = []
    
    for activo in activos:
        item = {
            "activo": activo,
            "riesgos": []
        }
        riesgos = list(mongo.db.riesgos.find({"activo_id": str(activo["_id"])}))
        
        for riesgo in riesgos:
            riesgo_item = {
                "detalle": riesgo,
                "tratamientos": list(mongo.db.tratamientos.find({"riesgo_id": str(riesgo["_id"])})),
                "residual": list(mongo.db.Residual.find({"riesgo_id": str(riesgo["_id"])}))
            }
            item["riesgos"].append(riesgo_item)
            
        reporte.append(item)
        
    return reporte
