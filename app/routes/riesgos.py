from flask import Blueprint, request, jsonify
from app.services.riesgo_service import crear_riesgo

riesgos_bp = Blueprint("riesgos", __name__)

@riesgos_bp.route("/", methods=["POST"], strict_slashes=False)
def crear():
    data = request.json
    try:
        return jsonify(crear_riesgo(data)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@riesgos_bp.route("/", methods=["GET"], strict_slashes=False)
def listar():
    try:
        from app.services.riesgo_service import obtener_riesgos
        return jsonify(obtener_riesgos()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@riesgos_bp.route("/<id>", methods=["PUT"], strict_slashes=False)
def actualizar(id):
    data = request.json
    try:
        from app.services.riesgo_service import actualizar_riesgo
        return jsonify(actualizar_riesgo(id, data)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@riesgos_bp.route("/<id>", methods=["DELETE"], strict_slashes=False)
def eliminar(id):
    try:
        from app.services.riesgo_service import eliminar_riesgo
        return jsonify(eliminar_riesgo(id)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
