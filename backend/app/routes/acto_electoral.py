from flask import Blueprint, request, jsonify
from app.controllers.acto_electoral_controller import registrar_acto_electoral

acto_bp = Blueprint('acto', __name__)

@acto_bp.route('/acto_electoral/registrar', methods=['POST'])
def registrar():
    data = request.get_json()
    resultado = registrar_acto_electoral(data)

    if resultado == 'CIUDADANO_NO_EXISTE':
        return jsonify({"error": "El ciudadano no existe"}), 400
    if resultado == 'ELECCION_NO_EXISTE':
        return jsonify({"error": "La elección no existe"}), 400
    if resultado == 'YA_VOTO':
        return jsonify({"error": "El ciudadano ya votó en esta elección"}), 400

    if resultado:
        return jsonify({"message": "Acto electoral registrado correctamente"}), 201
    return jsonify({"error": "No se pudo registrar el acto electoral"}), 500
