from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    mongo.init_app(app)

    from app.routes.activos import activos_bp
    from app.routes.riesgos import riesgos_bp
    from app.routes.tratamientos import tratamientos_bp
    from app.routes.residual import residual_bp
    from app.routes.comunicacion import comunicacion_bp

    app.register_blueprint(activos_bp, url_prefix="/activos")
    app.register_blueprint(riesgos_bp, url_prefix="/riesgos")
    app.register_blueprint(tratamientos_bp, url_prefix="/tratamientos")
    app.register_blueprint(residual_bp, url_prefix="/Residual")
    app.register_blueprint(comunicacion_bp, url_prefix="/Comunicacion")

    from app.routes.views import views_bp
    app.register_blueprint(views_bp)

    return app


print("APP PACKAGE CARGADO")