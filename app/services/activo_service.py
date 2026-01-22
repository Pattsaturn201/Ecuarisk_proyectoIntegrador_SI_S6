from app import mongo
from bson import ObjectId

def validar_activo(data):
    campos_obligatorios = [
        "nombre", "tipo", "area", "responsable", "descripcion",
        "confidencialidad", "integridad", "disponibilidad"
    ]

    for campo in campos_obligatorios:
        if campo not in data:
            raise ValueError(f"Falta el campo obligatorio: {campo}")

    for campo in ["confidencialidad", "integridad", "disponibilidad"]:
        valor = data.get(campo)
        if not str(valor).isdigit() or not (1 <= int(valor) <= 4):
            raise ValueError(f"{campo} debe estar entre 1 y 4")

def calcular_valor_activo(conf, integ, disp):
    return round((conf + integ + disp) / 3, 2)

def clasificar_activo(valor):
    if valor >= 3.5:
        return "Crítico"
    elif valor >= 2.5:
        return "Alto"
    elif valor >= 1.5:
        return "Medio"
    else:
        return "Bajo"

def crear_activo(data):
    validar_activo(data)

    conf = int(data["confidencialidad"])
    integ = int(data["integridad"])
    disp = int(data["disponibilidad"])

    valor = calcular_valor_activo(conf, integ, disp)
    clasificacion = clasificar_activo(valor)

    nuevo_activo = {
        "nombre": data["nombre"],
        "tipo": data["tipo"],
        "area": data["area"],
        "responsable": data["responsable"],
        "descripcion": data["descripcion"],
        "valoracion": {
            "confidencialidad": conf,
            "integridad": integ,
            "disponibilidad": disp
        },
        "valor_calculado": valor,
        "clasificacion": clasificacion
    }

    resultado = mongo.db.activos.insert_one(nuevo_activo)
    nuevo_activo["_id"] = str(resultado.inserted_id)
    
    return nuevo_activo

def obtener_activos():
    activos_cursor = mongo.db.activos.find()
    activos = []
    for activo in activos_cursor:
        activo["_id"] = str(activo["_id"])
        activos.append(activo)
    return activos

def actualizar_activo(id, data):
    validar_activo(data)
    
    # Recalcular valores
    conf = int(data["confidencialidad"])
    integ = int(data["integridad"])
    disp = int(data["disponibilidad"])
    valor = calcular_valor_activo(conf, integ, disp)
    clasificacion = clasificar_activo(valor)
    
    update_data = {
        "nombre": data["nombre"],
        "tipo": data["tipo"],
        "area": data["area"],
        "responsable": data["responsable"],
        "descripcion": data["descripcion"],
        "valoracion": {
            "confidencialidad": conf,
            "integridad": integ,
            "disponibilidad": disp
        },
        "valor_calculado": valor,
        "clasificacion": clasificacion
    }
    
    mongo.db.activos.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    update_data["_id"] = id
    return update_data

def eliminar_activo(id):
    mongo.db.activos.delete_one({"_id": ObjectId(id)})
    return {"mensaje": "Activo eliminado"}

