from flask import Blueprint, render_template

views_bp = Blueprint("views", __name__)

@views_bp.route("/")
def index():
    return render_template("index.html")

@views_bp.route("/view/activos")
def activos():
    return render_template("activos.html")

@views_bp.route("/view/riesgos")
def riesgos():
    return render_template("riesgos.html")

@views_bp.route("/view/tratamientos")
def tratamientos():
    return render_template("tratamientos.html")

@views_bp.route("/view/residual")
def residual():
    return render_template("residual.html")

@views_bp.route("/view/reporte")
def reporte():
    return render_template("reporte.html")
