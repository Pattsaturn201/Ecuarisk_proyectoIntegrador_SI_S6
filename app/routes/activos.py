from flask import Blueprint, request, jsonify
from app.services.activo_service import create_activo, get_activos

activos_bp = Blueprint("activos_bp", __name__)

@activos_bp.route("/", methods=["POST"])
def create():
    data = request.json
    return jsonify(create_activo(data)), 201

@activos_bp.route("/", methods=["GET"])
def list_all():
    return jsonify(get_activos())
