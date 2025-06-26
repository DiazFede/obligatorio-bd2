from flask import Blueprint, request, jsonify
from app.controllers.papeleta_controller import crear_papeleta, obtener_papeletas

papeleta_bp = Blueprint('papeleta', __name__)

@papeleta_bp.route('/papeleta/crear', methods=['POST'])
def crear():
    data = request.get_json()
    resultado = crear_papeleta(data)

    if resultado == 'LISTA_NO_EXISTE':
        return jsonify({"error": "La lista indicada no existe"}), 400
    if resultado == 'YA_EXISTE':
        return jsonify({"error": "Ya existe una papeleta para esta lista"}), 400
    if resultado:
        return jsonify({"message": "Papeleta creada correctamente"}), 201
    return jsonify({"error": "No se pudo crear la papeleta"}), 500

@papeleta_bp.route("/listas/papeletas", methods=["GET"])
def get_all_papeletas():
    return jsonify(obtener_papeletas())
