from flask import Blueprint, request, jsonify
from app.services.residual_service import calcular_residual

residual_bp = Blueprint("residual", __name__)

@residual_bp.route("/", methods=["POST"], strict_slashes=False)
def calcular():
    data = request.json
    try:
        return jsonify(calcular_residual(data)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@residual_bp.route("/", methods=["GET"], strict_slashes=False)
def listar():
    try:
        from app.services.residual_service import obtener_residuales
        return jsonify(obtener_residuales()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
