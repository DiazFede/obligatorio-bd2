from flask import Blueprint, request, jsonify
from app.controllers.departamento_controller import (
    crear_departamento,
    obtener_departamentos,
    obtener_departamento_por_id,
    actualizar_departamento,
    eliminar_departamento
)

departamento_bp = Blueprint('departamento', __name__)

@departamento_bp.route('/departamento', methods=['POST'])
def crear():
    data = request.get_json()
    resultado = crear_departamento(data)
    if resultado == 'YA_EXISTE':
        return jsonify({"error": "El departamento ya existe"}), 400
    if resultado:
        return jsonify({"message": "Departamento creado correctamente"}), 201
    return jsonify({"error": "No se pudo crear el departamento"}), 500

@departamento_bp.route('/departamento', methods=['GET'])
def listar():
    departamentos = obtener_departamentos()
    if departamentos:
        return jsonify(departamentos), 200
    return jsonify({"message": "No hay departamentos registrados"}), 404

@departamento_bp.route('/departamento/<int:id>', methods=['GET'])
def obtener(id):
    departamento = obtener_departamento_por_id(id)
    if departamento:
        return jsonify(departamento), 200
    return jsonify({"message": "Departamento no encontrado"}), 404

@departamento_bp.route('/departamento/<int:id>', methods=['PUT'])
def actualizar(id):
    data = request.get_json()
    resultado = actualizar_departamento(id, data)
    if resultado:
        return jsonify({"message": "Departamento actualizado correctamente"}), 200
    return jsonify({"error": "No se pudo actualizar el departamento"}), 500

@departamento_bp.route('/departamento/<int:id>', methods=['DELETE'])
def eliminar(id):
    resultado = eliminar_departamento(id)
    if resultado:
        return jsonify({"message": "Departamento eliminado correctamente"}), 200
    return jsonify({"error": "No se pudo eliminar el departamento"}), 500
