from flask import Blueprint, request, jsonify
from app.controllers.voto_controller import emitir_voto

voto_bp = Blueprint('voto', __name__, url_prefix='/voto')

@voto_bp.route("", methods=["POST"])
def votar():
    data = request.get_json()
    resultado = emitir_voto(data)

    if resultado == "YA_VOTO":
        return jsonify({"error": "Ya has votado en esta elección"}), 403
    if resultado == "NO_HABILITADO":
        return jsonify({"error": "No estás habilitado para esta elección"}), 403
    if resultado == "ELECCION_CERRADA":
        return jsonify({"error": "La elección está cerrada y no se puede votar"}), 403

    return jsonify({"mensaje": "Voto registrado correctamente"}), 201
