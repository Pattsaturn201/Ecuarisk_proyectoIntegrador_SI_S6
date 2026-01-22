from app import mongo
from bson import ObjectId

def validar_riesgo(data):
    campos_obligatorios = [
        "activo_id", "tipo_amenaza", "categoria", "descripcion",
        "controles_existentes", "probabilidad", "impacto"
    ]

    for campo in campos_obligatorios:
        if campo not in data:
            raise ValueError(f"Falta el campo obligatorio: {campo}")

    for campo in ["probabilidad", "impacto"]:
        valor = data.get(campo)
        if not str(valor).isdigit() or not (1 <= int(valor) <= 4):
            raise ValueError(f"{campo} debe estar entre 1 y 4")

def calcular_riesgo_inherente(prob, imp):
    return prob * imp

def clasificar_riesgo(valor):
    if valor >= 12:
        return "Critico"
    elif valor >= 8:
        return "Alto"
    elif valor >= 4:
        return "Medio"
    else:
        return "Bajo"

def crear_riesgo(data):
    validar_riesgo(data)

    # Validar existencia del activo
    try:
        activo_id = ObjectId(data["activo_id"])
    except:
         raise ValueError("ID de activo inválido")
         
    activo = mongo.db.activos.find_one({"_id": activo_id})
    if not activo:
        raise ValueError("Activo no encontrado")

    # Validar duplicidad
    existe = mongo.db.riesgos.find_one({
        "activo_id": activo_id, 
        "tipo_amenaza": data["tipo_amenaza"],
        "categoria": data["categoria"]
    })
    if existe:
        raise ValueError("Este riesgo ya está registrado para este activo")

    prob = int(data["probabilidad"])
    imp = int(data["impacto"])

    riesgo_inherente = calcular_riesgo_inherente(prob, imp)
    clasificacion = clasificar_riesgo(riesgo_inherente)

    nuevo_riesgo = {
        "activo_id": activo_id, # Almacenar como ObjectId
        "amenaza": data["tipo_amenaza"], # Schema espera "amenaza"
        "tipo_amenaza": data["tipo_amenaza"],
        "categoria": data["categoria"],
        "descripcion": data["descripcion"],
        "controles_existentes": data["controles_existentes"],
        "probabilidad": prob,
        "impacto": imp,
        "riesgo_inherente": riesgo_inherente,
        "clasificacion": clasificacion
    }

    resultado = mongo.db.riesgos.insert_one(nuevo_riesgo)
    nuevo_riesgo["_id"] = str(resultado.inserted_id)
    
    return nuevo_riesgo

def obtener_riesgos():
    riesgos_cursor = mongo.db.riesgos.find()
    riesgos = []
    
    # Cache activos para evitar muchas consultas
    mapa_activos = {}
    
    for riesgo in riesgos_cursor:
        riesgo["_id"] = str(riesgo["_id"])
        
        # Enriquecer con nombre del activo
        act_id = str(riesgo["activo_id"])
        if act_id not in mapa_activos:
            activo = mongo.db.activos.find_one({"_id": riesgo["activo_id"]})
            mapa_activos[act_id] = activo["nombre"] if activo else "Desconocido"
            
        riesgo["nombre_activo"] = mapa_activos[act_id]
        riesgo["activo_id"] = str(riesgo["activo_id"]) # Serializar
        riesgos.append(riesgo)
        
    return riesgos

def actualizar_riesgo(id, data):
    validar_riesgo(data)
    
    # Recalcular
    prob = int(data["probabilidad"])
    imp = int(data["impacto"])
    riesgo_inherente = calcular_riesgo_inherente(prob, imp)
    clasificacion = clasificar_riesgo(riesgo_inherente)
    
    update_data = {
        "tipo_amenaza": data["tipo_amenaza"],
        "amenaza": data["tipo_amenaza"],
        "categoria": data["categoria"],
        "descripcion": data["descripcion"],
        "controles_existentes": data["controles_existentes"],
        "probabilidad": prob,
        "impacto": imp,
        "riesgo_inherente": riesgo_inherente,
        "clasificacion": clasificacion
    }
    
    mongo.db.riesgos.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    update_data["_id"] = id
    return update_data

def eliminar_riesgo(id):
    mongo.db.riesgos.delete_one({"_id": ObjectId(id)})
    return {"mensaje": "Riesgo eliminado"}
