from flask import Blueprint, request, jsonify
from app.controllers.agente_controller import (
    crear_agente,
    obtener_agentes,
    obtener_agente_por_placa,
    actualizar_agente,
    eliminar_agente
)

agente_bp = Blueprint('agente', __name__)

@agente_bp.route('/agente', methods=['POST'])
def crear():
    data = request.get_json()
    resultado = crear_agente(data)
    if resultado == 'YA_EXISTE':
        return jsonify({"error": "El agente ya existe"}), 400
    if resultado == 'ESTABLECIMIENTO_NO_EXISTE':
        return jsonify({"error": "El establecimiento no existe"}), 400
    if resultado == 'COMISARIA_NO_EXISTE':
        return jsonify({"error": "La comisaría no existe"}), 400
    if resultado:
        return jsonify({"message": "Agente creado correctamente"}), 201
    return jsonify({"error": "No se pudo crear el agente"}), 500

@agente_bp.route('/agente', methods=['GET'])
def listar():
    agentes = obtener_agentes()
    if agentes:
        return jsonify(agentes), 200
    return jsonify({"message": "No hay agentes registrados"}), 404

@agente_bp.route('/agente/<int:numero_placa>', methods=['GET'])
def obtener(numero_placa):
    agente = obtener_agente_por_placa(numero_placa)
    if agente:
        return jsonify(agente), 200
    return jsonify({"message": "Agente no encontrado"}), 404

@agente_bp.route('/agente/<int:numero_placa>', methods=['PUT'])
def actualizar(numero_placa):
    data = request.get_json()
    resultado = actualizar_agente(numero_placa, data)
    if resultado == 'ESTABLECIMIENTO_NO_EXISTE':
        return jsonify({"error": "El establecimiento no existe"}), 400
    if resultado == 'COMISARIA_NO_EXISTE':
        return jsonify({"error": "La comisaría no existe"}), 400
    if resultado:
        return jsonify({"message": "Agente actualizado correctamente"}), 200
    return jsonify({"error": "No se pudo actualizar el agente"}), 500

@agente_bp.route('/agente/<int:numero_placa>', methods=['DELETE'])
def eliminar(numero_placa):
    resultado = eliminar_agente(numero_placa)
    if resultado:
        return jsonify({"message": "Agente eliminado correctamente"}), 200
    return jsonify({"error": "No se pudo eliminar el agente"}), 500
