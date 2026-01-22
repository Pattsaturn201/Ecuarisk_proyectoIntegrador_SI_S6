from flask import Blueprint, request, jsonify
from app.services.tratamiento_service import crear_tratamiento

tratamientos_bp = Blueprint("tratamientos", __name__)

@tratamientos_bp.route("/", methods=["POST"], strict_slashes=False)
def crear():
    data = request.json
    try:
        return jsonify(crear_tratamiento(data)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@tratamientos_bp.route("/", methods=["GET"], strict_slashes=False)
def listar():
    try:
        from app.services.tratamiento_service import obtener_tratamientos
        return jsonify(obtener_tratamientos()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@tratamientos_bp.route("/<id>", methods=["PUT"], strict_slashes=False)
def actualizar(id):
    data = request.json
    try:
        from app.services.tratamiento_service import actualizar_tratamiento
        return jsonify(actualizar_tratamiento(id, data)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@tratamientos_bp.route("/<id>", methods=["DELETE"], strict_slashes=False)
def eliminar(id):
    try:
        from app.services.tratamiento_service import eliminar_tratamiento
        return jsonify(eliminar_tratamiento(id)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
