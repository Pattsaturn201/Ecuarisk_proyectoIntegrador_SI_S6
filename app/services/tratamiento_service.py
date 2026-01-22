from app import mongo
from bson import ObjectId

def validar_tratamiento(data):
    if "riesgo_id" not in data:
        raise ValueError("Falta riesgo_id")
    if "estrategia" not in data:
        raise ValueError("Falta estrategia")
    if data["estrategia"] not in ["Mitigar", "Transferir", "Aceptar", "Evitar"]:
         raise ValueError("Estrategia inválida")
    
    if "controles_propuestos" not in data or not isinstance(data["controles_propuestos"], list):
        raise ValueError("Faltan controles propuestos o formato inválido")

    for control in data["controles_propuestos"]:
        required_control_fields = ["codigo_iso", "descripcion", "tipo", "responsable", "fecha_implementacion", "estado"]
        for field in required_control_fields:
            if field not in control:
                raise ValueError(f"Falta campo {field} en control")

def crear_tratamiento(data):
    validar_tratamiento(data)
    
    try:
        riesgo_id = ObjectId(data["riesgo_id"])
    except:
        raise ValueError("ID de riesgo inválido")
        
    riesgo = mongo.db.riesgos.find_one({"_id": riesgo_id})
    if not riesgo:
        raise ValueError("Riesgo no encontrado")
    
    nuevo_tratamiento = {
        "riesgo_id": riesgo_id,
        "estrategia": data["estrategia"],
        "controles_propuestos": data["controles_propuestos"]
    }
    
    resultado = mongo.db.tratamientos.insert_one(nuevo_tratamiento)
    nuevo_tratamiento["_id"] = str(resultado.inserted_id)
    nuevo_tratamiento["riesgo_id"] = str(nuevo_tratamiento["riesgo_id"])
    
    return nuevo_tratamiento

def obtener_tratamientos():
    cursor = mongo.db.tratamientos.find()
    tratamientos = []
    
    # Cache riesgos para evitar N+1 queries
    mapa_riesgos = {}
    
    for t in cursor:
        t["_id"] = str(t["_id"])
        r_id = str(t["riesgo_id"])
        
        if r_id not in mapa_riesgos:
            riesgo = mongo.db.riesgos.find_one({"_id": t["riesgo_id"]})
            if riesgo:
                # Obtener nombre activo si es posible, o usar descripcion
                activo_nombre = "Desconocido"
                try:
                    activo = mongo.db.activos.find_one({"_id": riesgo["activo_id"]})
                    if activo:
                        activo_nombre = activo["nombre"]
                except:
                    pass
                mapa_riesgos[r_id] = f"{riesgo['descripcion'][:30]}... ({activo_nombre})"
            else:
                mapa_riesgos[r_id] = "Riesgo no encontrado"
        
        t["detalle_riesgo"] = mapa_riesgos[r_id]
        t["riesgo_id"] = str(t["riesgo_id"])
        tratamientos.append(t)
        
    return tratamientos

def actualizar_tratamiento(id, data):
    validar_tratamiento(data)
    
    try:
        riesgo_id = ObjectId(data["riesgo_id"])
    except:
        raise ValueError("ID de riesgo inválido")

    nuevo_tratamiento = {
        "riesgo_id": riesgo_id,
        "estrategia": data["estrategia"],
        "controles_propuestos": data["controles_propuestos"]
    }
    
    mongo.db.tratamientos.update_one({"_id": ObjectId(id)}, {"$set": nuevo_tratamiento})
    nuevo_tratamiento["_id"] = id
    nuevo_tratamiento["riesgo_id"] = str(riesgo_id)
    return nuevo_tratamiento

def eliminar_tratamiento(id):
    mongo.db.tratamientos.delete_one({"_id": ObjectId(id)})
    return {"mensaje": "Tratamiento eliminado"}
