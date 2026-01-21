from flask import Blueprint, request, jsonify
from app.services.tratamiento_service import crear_tratamiento

tratamientos_bp = Blueprint("tratamientos_bp", __name__)

@tratamientos_bp.route("/", methods=["POST"])
def crear():
    respuesta = crear_tratamiento(request.json)
    return jsonify(respuesta)

@tratamientos_bp.route("/<id>/estado", methods=["PUT"])
def actualizar_estado(id):
    data = request.json
    return jsonify(actualizar_estado_tratamiento(id, data["estado"]))