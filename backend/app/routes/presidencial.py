from flask import Blueprint, jsonify
from app.controllers.presidencial_controller import obtener_listas_presidenciales

presidencial_bp = Blueprint('presidencial', __name__)

@presidencial_bp.route("/listas/presidenciales", methods=["GET"])
def get_all_presidenciales():
    return jsonify(obtener_listas_presidenciales())