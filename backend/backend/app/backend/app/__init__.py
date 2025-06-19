
from flask import Flask
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Importar y registrar Blueprints
    from app.routes.auth import auth_bp
    from app.routes.voto import voto_bp
    from app.routes.resultados import resultados_bp
    # from app.routes.eleccion import eleccion_bp # Para futuras rutas de gestión de elecciones
    # from app.routes.admin import admin_bp       # Para futuras rutas de administración

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(voto_bp, url_prefix='/api/voto')
    app.register_blueprint(resultados_bp, url_prefix='/api/resultados')
    # app.register_blueprint(eleccion_bp, url_prefix='/api/elecciones')
    # app.register_blueprint(admin_bp, url_prefix='/api/admin')

    return app