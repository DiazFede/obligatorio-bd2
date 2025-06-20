from flask import Blueprint, request, jsonify
from app.controllers.establecimiento_controller import (
    crear_establecimiento,
    obtener_establecimientos,
    obtener_establecimiento_por_numero,
    actualizar_establecimiento,
    eliminar_establecimiento
)

establecimiento_bp = Blueprint('establecimiento', __name__)

@establecimiento_bp.route('/establecimiento', methods=['POST'])
def crear():
    data = request.get_json()
    resultado = crear_establecimiento(data)
    if resultado == 'ZONA_NO_EXISTE':
        return jsonify({"error": "La zona especificada no existe"}), 400
    if resultado == 'YA_EXISTE':
        return jsonify({"error": "El establecimiento ya existe"}), 400
    if resultado:
        return jsonify({"message": "Establecimiento creado correctamente"}), 201
    return jsonify({"error": "No se pudo crear el establecimiento"}), 500

@establecimiento_bp.route('/establecimiento', methods=['GET'])
def listar():
    establecimientos = obtener_establecimientos()
    if establecimientos:
        return jsonify(establecimientos), 200
    return jsonify({"message": "No hay establecimientos registrados"}), 404

@establecimiento_bp.route('/establecimiento/<int:numero_establecimiento>', methods=['GET'])
def obtener(numero_establecimiento):
    establecimiento = obtener_establecimiento_por_numero(numero_establecimiento)
    if establecimiento:
        return jsonify(establecimiento), 200
    return jsonify({"message": "Establecimiento no encontrado"}), 404

@establecimiento_bp.route('/establecimiento/<int:numero_establecimiento>', methods=['PUT'])
def actualizar(numero_establecimiento):
    data = request.get_json()
    resultado = actualizar_establecimiento(numero_establecimiento, data)
    if resultado == 'ZONA_NO_EXISTE':
        return jsonify({"error": "La zona especificada no existe"}), 400
    if resultado:
        return jsonify({"message": "Establecimiento actualizado correctamente"}), 200
    return jsonify({"error": "No se pudo actualizar el establecimiento"}), 500

@establecimiento_bp.route('/establecimiento/<int:numero_establecimiento>', methods=['DELETE'])
def eliminar(numero_establecimiento):
    resultado = eliminar_establecimiento(numero_establecimiento)
    if resultado:
        return jsonify({"message": "Establecimiento eliminado correctamente"}), 200
    return jsonify({"error": "No se pudo eliminar el establecimiento"}), 500
