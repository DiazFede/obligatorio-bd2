from flask import Blueprint, request, jsonify
from app.controllers.partido_controller import crear_partido

partido_bp = Blueprint('partido', __name__)

@partido_bp.route('/partido/crear', methods=['POST'])
def crear():
    data = request.get_json()
    resultado = crear_partido(data)
    if resultado == 'YA_EXISTE':
        return jsonify({"error": "El partido ya existe"}), 400
    if resultado:
        return jsonify({"message": "Partido creado correctamente"}), 201
    return jsonify({"error": "No se pudo crear el partido"}), 500
