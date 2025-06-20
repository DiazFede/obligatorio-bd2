from flask import Blueprint, request, jsonify
from app.controllers.candidato_controller import registrar_candidato

candidato_bp = Blueprint('candidato', __name__)

@candidato_bp.route('/candidato/registrar', methods=['POST'])
def registrar():
    data = request.get_json()
    resultado = registrar_candidato(data)

    if resultado == 'CIUDADANO_NO_EXISTE':
        return jsonify({"error": "El ciudadano no existe"}), 400
    if resultado == 'PARTIDO_NO_EXISTE':
        return jsonify({"error": "El partido político no existe"}), 400
    if resultado:
        return jsonify({"message": "Candidato registrado con éxito"}), 201
    return jsonify({"error": "No se pudo registrar el candidato"}), 500
