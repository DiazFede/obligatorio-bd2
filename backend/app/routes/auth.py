from flask import Blueprint, request, jsonify
from app.controllers.auth_controller import registrar_ciudadano, obtener_ciudadano

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/registrar', methods=['POST'])
def registrar():
    data = request.json
    resultado = registrar_ciudadano(data)
    if resultado:
        return jsonify({'mensaje': 'Ciudadano registrado correctamente'}), 201
    return jsonify({'error': 'No se pudo registrar al ciudadano'}), 500

@auth_bp.route('/<int:credencial>', methods=['GET'])
def ver_ciudadano(credencial):
    ciudadano = obtener_ciudadano(credencial)
    if ciudadano:
        return jsonify(ciudadano), 200
    return jsonify({'error': 'Ciudadano no encontrado'}), 404
