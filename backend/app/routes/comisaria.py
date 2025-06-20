from flask import Blueprint, request, jsonify
from app.controllers.comisaria_controller import (
    crear_comisaria,
    obtener_comisarias,
    obtener_comisaria_por_id,
    actualizar_comisaria,
    eliminar_comisaria
)

comisaria_bp = Blueprint('comisaria', __name__)

@comisaria_bp.route('/comisaria', methods=['POST'])
def crear():
    data = request.get_json()
    resultado = crear_comisaria(data)
    if resultado == 'YA_EXISTE':
        return jsonify({"error": "La comisaría ya existe"}), 400
    if resultado:
        return jsonify({"message": "Comisaría creada correctamente"}), 201
    return jsonify({"error": "No se pudo crear la comisaría"}), 500

@comisaria_bp.route('/comisaria', methods=['GET'])
def listar():
    comisarias = obtener_comisarias()
    if comisarias:
        return jsonify(comisarias), 200
    return jsonify({"message": "No hay comisarías registradas"}), 404

@comisaria_bp.route('/comisaria/<int:id_comisaria>', methods=['GET'])
def obtener(id_comisaria):
    comisaria = obtener_comisaria_por_id(id_comisaria)
    if comisaria:
        return jsonify(comisaria), 200
    return jsonify({"message": "Comisaría no encontrada"}), 404

@comisaria_bp.route('/comisaria/<int:id_comisaria>', methods=['PUT'])
def actualizar(id_comisaria):
    data = request.get_json()
    resultado = actualizar_comisaria(id_comisaria, data)
    if resultado:
        return jsonify({"message": "Comisaría actualizada correctamente"}), 200
    return jsonify({"error": "No se pudo actualizar la comisaría"}), 500

@comisaria_bp.route('/comisaria/<int:id_comisaria>', methods=['DELETE'])
def eliminar(id_comisaria):
    resultado = eliminar_comisaria(id_comisaria)
    if resultado:
        return jsonify({"message": "Comisaría eliminada correctamente"}), 200
    return jsonify({"error": "No se pudo eliminar la comisaría"}), 500
