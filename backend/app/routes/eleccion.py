from flask import Blueprint, request, jsonify
from app.controllers.eleccion_controller import crear_eleccion, obtener_eleccion

eleccion_bp = Blueprint('eleccion', __name__, url_prefix='/eleccion')

@eleccion_bp.route('/crear', methods=['POST'])
def crear():
    data = request.json
    resultado = crear_eleccion(data)
    if resultado:
        return jsonify({'mensaje': 'Elección registrada correctamente'}), 201
    return jsonify({'error': 'No se pudo registrar la elección'}), 500

@eleccion_bp.route('/<int:id_eleccion>', methods=['GET'])
def ver(id_eleccion):
    eleccion = obtener_eleccion(id_eleccion)
    if eleccion:
        return jsonify(eleccion), 200
    return jsonify({'error': 'Elección no encontrada'}), 404
