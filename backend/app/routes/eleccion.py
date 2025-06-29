from flask import Blueprint, request, jsonify
from app.controllers.eleccion_controller import (
    crear_eleccion,
    obtener_eleccion,
    elecciones_disponibles,
    cambiar_estado_eleccion,
    obtener_todas_las_elecciones
)

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

@eleccion_bp.route('/', methods=['GET'])
def listar_elecciones():
    elecciones = obtener_todas_las_elecciones()
    return jsonify(elecciones), 200

@eleccion_bp.route("/<numero_credencial>", methods=["GET"])
def obtener_elecciones(numero_credencial):
    return jsonify(elecciones_disponibles(numero_credencial))

@eleccion_bp.route('/<int:id_eleccion>/status', methods=['PUT'])
def actualizar_estado_eleccion(id_eleccion):
    data = request.get_json()
    nuevo_estado = data.get("status")

    if nuevo_estado not in [0, 1, True, False]:
        return jsonify({"error": "Estado inválido"}), 400

    eleccion = obtener_eleccion(id_eleccion)
    if not eleccion:
        return jsonify({"error": "Elección no encontrada"}), 404

    estado_actual = eleccion['status']

    if estado_actual == False and nuevo_estado == True:
        return jsonify({"error": "No se puede reabrir una elección una vez cerrada"}), 403

    cambiar_estado_eleccion(id_eleccion, nuevo_estado)
    estado_str = "abierta" if nuevo_estado else "cerrada"
    return jsonify({"mensaje": f"Elección marcada como {estado_str} correctamente"}), 200
