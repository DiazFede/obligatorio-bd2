from flask import Blueprint, request, jsonify
from app.controllers.ballotage_controller import crear_lista_ballotage

ballotage_bp = Blueprint('ballotage', __name__)

@ballotage_bp.route('/lista/ballotage', methods=['POST'])
def crear():
    data = request.get_json()
    resultado = crear_lista_ballotage(data)
    if resultado == 'LISTA_NO_EXISTE':
        return jsonify({"error": "La lista base no existe"}), 400
    if resultado == 'YA_EXISTE':
        return jsonify({"error": "Ya existe una lista ballotage con ese ID"}), 400
    if resultado:
        return jsonify({"message": "Lista ballotage registrada correctamente"}), 201
    return jsonify({"error": "No se pudo registrar la lista ballotage"}), 500
