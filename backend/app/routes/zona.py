from flask import Blueprint, request, jsonify
from app.controllers.zona_controller import (
    crear_zona,
    obtener_zonas,
    obtener_zona_por_numero,
    actualizar_zona,
    eliminar_zona
)

zona_bp = Blueprint('zona', __name__)

@zona_bp.route('/zona', methods=['POST'])
def crear():
    data = request.get_json()
    resultado = crear_zona(data)
    if resultado == 'DEPARTAMENTO_NO_EXISTE':
        return jsonify({"error": "El departamento especificado no existe"}), 400
    if resultado == 'YA_EXISTE':
        return jsonify({"error": "La zona ya existe"}), 400
    if resultado:
        return jsonify({"message": "Zona creada correctamente"}), 201
    return jsonify({"error": "No se pudo crear la zona"}), 500

@zona_bp.route('/zona', methods=['GET'])
def listar():
    zonas = obtener_zonas()
    if zonas:
        return jsonify(zonas), 200
    return jsonify({"message": "No hay zonas registradas"}), 404

@zona_bp.route('/zona/<int:numero_zona>', methods=['GET'])
def obtener(numero_zona):
    zona = obtener_zona_por_numero(numero_zona)
    if zona:
        return jsonify(zona), 200
    return jsonify({"message": "Zona no encontrada"}), 404

@zona_bp.route('/zona/<int:numero_zona>', methods=['PUT'])
def actualizar(numero_zona):
    data = request.get_json()
    resultado = actualizar_zona(numero_zona, data)
    if resultado == 'DEPARTAMENTO_NO_EXISTE':
        return jsonify({"error": "El departamento especificado no existe"}), 400
    if resultado:
        return jsonify({"message": "Zona actualizada correctamente"}), 200
    return jsonify({"error": "No se pudo actualizar la zona"}), 500

@zona_bp.route('/zona/<int:numero_zona>', methods=['DELETE'])
def eliminar(numero_zona):
    resultado = eliminar_zona(numero_zona)
    if resultado:
        return jsonify({"message": "Zona eliminada correctamente"}), 200
    return jsonify({"error": "No se pudo eliminar la zona"}), 500
