from flask import Blueprint, request, jsonify
from app.db import insert_data, get_one

acto_electoral_bp = Blueprint('acto_electoral', __name__, url_prefix='/acto-electoral')

@acto_electoral_bp.route('/autorizar', methods=['POST'])
def autorizar_ciudadano():
    data = request.get_json()
    numero_credencial = data.get("numero_credencial")
    id_eleccion = data.get("id_eleccion")
    numero_circuito = data.get("numero_circuito")

    if not numero_credencial or not id_eleccion or not numero_circuito:
        return jsonify({"error": "Datos incompletos"}), 400

    ciudadano = get_one("SELECT 1 FROM Ciudadano WHERE numero_credencial = %s", (numero_credencial,))
    if not ciudadano:
        return jsonify({"error": "La credencial no existe"}), 404

    eleccion = get_one("SELECT 1 FROM Eleccion WHERE id_eleccion = %s", (id_eleccion,))
    if not eleccion:
        return jsonify({"error": "La elección no existe"}), 404

    circuito = get_one("SELECT 1 FROM Circuito WHERE numero_circuito = %s", (numero_circuito,))
    if not circuito:
        return jsonify({"error": "El circuito no existe"}), 404

    query = """
        INSERT INTO Acto_Electoral (numero_credencial, id_eleccion, numero_circuito)
        VALUES (%s, %s, %s)
    """
    insert_data(query, (numero_credencial, id_eleccion, numero_circuito))

    return jsonify({"mensaje": "Ciudadano autorizado correctamente"}), 201
