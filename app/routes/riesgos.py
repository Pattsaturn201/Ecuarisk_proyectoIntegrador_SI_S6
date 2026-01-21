from flask import Blueprint, request, jsonify
from app.services.riesgo_service import create_riesgo, get_riesgos

riesgos_bp = Blueprint("riesgos_bp", __name__)

@riesgos_bp.route("/", methods=["POST"])
def create():
    return jsonify(create_riesgo(request.json)), 201

@riesgos_bp.route("/", methods=["GET"])
def list_all():
    return jsonify(get_riesgos())
