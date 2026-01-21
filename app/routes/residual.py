from flask import Blueprint, request, jsonify
from app.services.riesgo_residual_service import calcular_riesgo_residual

residual_bp = Blueprint("residual_bp", __name__)

@residual_bp.route("/", methods=["POST"])
def crear():
    return jsonify(calcular_riesgo_residual(request.json)), 201


