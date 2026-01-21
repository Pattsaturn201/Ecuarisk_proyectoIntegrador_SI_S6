from flask import Blueprint, request, jsonify
from app.services.observacion_service import crear_observacion

comunicacion_bp = Blueprint("comunicacion_bp", __name__)

@comunicacion_bp.route("/", methods=["POST"])
def crear():
    return jsonify(crear_observacion(request.json)), 201
