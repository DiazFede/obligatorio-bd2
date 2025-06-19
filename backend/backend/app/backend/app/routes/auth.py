from flask import Blueprint, request, jsonify
from app.controllers.auth_controller import registrar_ciudadano, iniciar_sesion

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    response, status_code = registrar_ciudadano(data)
    return jsonify(response), status_code

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    response, status_code = iniciar_sesion(data)
    return jsonify(response), status_code