from flask import Flask
from app.routes.auth import auth_bp
from app.routes.eleccion import eleccion_bp
from app.routes.voto import voto_bp
from app.routes.resultados import resultados_bp
from app.routes.candidato import candidato_bp
from app.routes.partido import partido_bp
from app.routes.mesa import mesa_bp
from app.routes.acto_electoral import acto_bp
from app.routes.lista import lista_bp
from app.routes.papeleta import papeleta_bp
from app.routes.municipal import municipal_bp
from app.routes.ballotage import ballotage_bp
from app.routes.establecimiento import establecimiento_bp
from app.routes.zona import zona_bp
from app.routes.departamento import departamento_bp
from app.routes.establecimiento_eleccion import establecimiento_eleccion_bp
from app.routes.comisaria import comisaria_bp
from app.routes.agente import agente_bp



def create_app():
    app = Flask(__name__)
    app.register_blueprint(auth_bp)
    app.register_blueprint(eleccion_bp)
    app.register_blueprint(voto_bp)
    app.register_blueprint(resultados_bp, url_prefix='/resultados')
    app.register_blueprint(candidato_bp)
    app.register_blueprint(partido_bp)
    app.register_blueprint(mesa_bp)
    app.register_blueprint(acto_bp)
    app.register_blueprint(lista_bp)
    app.register_blueprint(papeleta_bp)
    app.register_blueprint(municipal_bp)
    app.register_blueprint(ballotage_bp)
    app.register_blueprint(establecimiento_bp)
    app.register_blueprint(zona_bp)
    app.register_blueprint(departamento_bp)
    app.register_blueprint(establecimiento_eleccion_bp)
    app.register_blueprint(comisaria_bp)
    app.register_blueprint(agente_bp)
    return app
