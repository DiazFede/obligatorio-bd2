from flask import Blueprint, request, jsonify
from app.controllers.auth_controller import registrar_ciudadano, login_ciudadano
from flask_jwt_extended import jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/registrar', methods=['POST'])
def registrar():
    data = request.get_json()
    resultado = registrar_ciudadano(data)
    if resultado:
        return jsonify({"mensaje": "Ciudadano registrado correctamente"}), 201
    return jsonify({"error": "El número de credencial ya existe"}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    resultado = login_ciudadano(data)
    if resultado:
        return jsonify(resultado), 200
    return jsonify({"error": "Credenciales inválidas"}), 401

@auth_bp.route('/perfil', methods=['GET'])
@jwt_required()
def perfil():
    numero_credencial = get_jwt_identity()
    return jsonify({"mensaje": f"Acceso autorizado para ciudadano con credencial {numero_credencial}"})
