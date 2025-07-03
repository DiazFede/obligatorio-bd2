from flask import Flask
from app.routes.auth import auth_bp
from app.routes.eleccion import eleccion_bp
from app.routes.voto import voto_bp
from app.routes.resultados import resultados_bp
from app.routes.acto_electoral import acto_electoral_bp
from app.routes.lista import lista_bp
from app.routes.papeleta import papeleta_bp
from app.routes.municipal import municipal_bp
from app.routes.ballotage import ballotage_bp
from app.routes.presidencial import presidencial_bp
from app.routes.admin import admin_bp
from app.routes.estadisticas import estadisticas_bp
from flask_jwt_extended import JWTManager
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object("app.config.Config")

    jwt = JWTManager(app)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(eleccion_bp)
    app.register_blueprint(voto_bp)
    app.register_blueprint(resultados_bp, url_prefix='/resultados')
    app.register_blueprint(acto_electoral_bp)
    app.register_blueprint(lista_bp)
    app.register_blueprint(papeleta_bp)
    app.register_blueprint(municipal_bp)
    app.register_blueprint(ballotage_bp)
    app.register_blueprint(presidencial_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(estadisticas_bp)
    return app
