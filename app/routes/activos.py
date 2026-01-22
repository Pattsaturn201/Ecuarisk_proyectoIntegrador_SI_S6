from flask import Blueprint, request, jsonify
from app.services.activo_service import crear_activo

activos_bp = Blueprint("activos", __name__)

@activos_bp.route("/", methods=["POST"], strict_slashes=False)
def crear():
    data = request.json
    try:
        return jsonify(crear_activo(data)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@activos_bp.route("/", methods=["GET"], strict_slashes=False)
def listar():
    try:
        from app.services.activo_service import obtener_activos
        return jsonify(obtener_activos()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@activos_bp.route("/<id>", methods=["PUT"], strict_slashes=False)
def actualizar(id):
    data = request.json
    try:
        from app.services.activo_service import actualizar_activo
        return jsonify(actualizar_activo(id, data)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@activos_bp.route("/<id>", methods=["DELETE"], strict_slashes=False)
def eliminar(id):
    try:
        from app.services.activo_service import eliminar_activo
        return jsonify(eliminar_activo(id)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
