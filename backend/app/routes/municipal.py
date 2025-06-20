from flask import Blueprint, request, jsonify
from app.controllers.municipal_controller import crear_lista_municipal

municipal_bp = Blueprint('municipal', __name__)

@municipal_bp.route('/lista/municipal', methods=['POST'])
def crear():
    data = request.get_json()
    resultado = crear_lista_municipal(data)
    if resultado == 'LISTA_NO_EXISTE':
        return jsonify({"error": "La lista base no existe"}), 400
    if resultado == 'YA_EXISTE':
        return jsonify({"error": "Ya existe una lista municipal con ese ID"}), 400
    if resultado:
        return jsonify({"message": "Lista municipal registrada correctamente"}), 201
    return jsonify({"error": "No se pudo registrar la lista municipal"}), 500
