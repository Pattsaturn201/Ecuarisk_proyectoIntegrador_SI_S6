from flask import Blueprint, request, jsonify
from app.services.comunicacion_service import crear_comunicacion, obtener_reporte_completo

comunicacion_bp = Blueprint("comunicacion", __name__)

@comunicacion_bp.route("/", methods=["POST"])
def crear():
    try:
        data = request.json
        return jsonify(crear_comunicacion(data)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@comunicacion_bp.route("/reporte", methods=["GET"])
def reporte():
    try:
        return jsonify(obtener_reporte_completo()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
