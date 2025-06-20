from flask import Blueprint, request, jsonify
from app.controllers.establecimiento_eleccion_controller import (
    crear_establecimiento_eleccion,
    obtener_establecimientos_eleccion,
    eliminar_establecimiento_eleccion
)

establecimiento_eleccion_bp = Blueprint('establecimiento_eleccion', __name__)

@establecimiento_eleccion_bp.route('/establecimiento_eleccion', methods=['POST'])
def crear():
    data = request.get_json()
    resultado = crear_establecimiento_eleccion(data)

    if resultado == 'ESTABLECIMIENTO_NO_EXISTE':
        return jsonify({"error": "El establecimiento no existe"}), 400
    if resultado == 'ELECCION_NO_EXISTE':
        return jsonify({"error": "La elección no existe"}), 400
    if resultado == 'CIRCUITO_NO_EXISTE':
        return jsonify({"error": "El circuito no existe"}), 400
    if resultado == 'YA_EXISTE':
        return jsonify({"error": "La combinación ya existe"}), 400
    if resultado:
        return jsonify({"message": "Establecimiento - Elección creado correctamente"}), 201
    return jsonify({"error": "No se pudo crear la relación"}), 500

@establecimiento_eleccion_bp.route('/establecimiento_eleccion', methods=['GET'])
def listar():
    registros = obtener_establecimientos_eleccion()
    if registros:
        return jsonify(registros), 200
    return jsonify({"message": "No hay registros"}), 404

@establecimiento_eleccion_bp.route('/establecimiento_eleccion/<int:numero_establecimiento>/<int:id_eleccion>/<int:numero_circuito>', methods=['DELETE'])
def eliminar(numero_establecimiento, id_eleccion, numero_circuito):
    resultado = eliminar_establecimiento_eleccion(numero_establecimiento, id_eleccion, numero_circuito)
    if resultado:
        return jsonify({"message": "Registro eliminado correctamente"}), 200
    return jsonify({"error": "No se pudo eliminar el registro"}), 500
