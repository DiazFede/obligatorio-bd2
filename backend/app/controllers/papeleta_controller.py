from app.db import insert_data, get_one, get_all

def crear_papeleta(data):
    lista = get_one("SELECT 1 FROM Lista WHERE id = %s", (data['id'],))
    if not lista:
        return 'LISTA_NO_EXISTE'

    existente = get_one("SELECT 1 FROM Papeleta WHERE id = %s", (data['id'],))
    if existente:
        return 'YA_EXISTE'

    query = "INSERT INTO Papeleta (id, opcion) VALUES (%s, %s)"
    return insert_data(query, (data['id'], data['opcion']))

from flask import Blueprint, request, jsonify
from app.controllers.papeleta_controller import crear_papeleta

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

def obtener_papeletas():
    return get_all("SELECT * FROM Lista NATURAL JOIN Papeleta")