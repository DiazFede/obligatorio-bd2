from flask import Blueprint, request, jsonify
from app.controllers.lista_controller import (
    crear_lista,
    agregar_papeleta,
    registrar_lista_presidencial,
    registrar_lista_ballotage,
    registrar_lista_municipal
)

lista_bp = Blueprint('lista', __name__)

@lista_bp.route('/lista/crear', methods=['POST'])
def crear():
    data = request.get_json()
    resultado = crear_lista(data)
    if resultado == 'YA_EXISTE':
        return jsonify({"error": "La lista ya existe"}), 400
    if resultado:
        return jsonify({"message": "Lista creada correctamente"}), 201
    return jsonify({"error": "No se pudo crear la lista"}), 500

@lista_bp.route('/papeleta/agregar', methods=['POST'])
def agregar():
    data = request.get_json()
    resultado = agregar_papeleta(data)
    if resultado == 'YA_EXISTE':
        return jsonify({"error": "La papeleta ya existe"}), 400
    if resultado:
        return jsonify({"message": "Papeleta agregada correctamente"}), 201
    return jsonify({"error": "No se pudo agregar la papeleta"}), 500

@lista_bp.route('/lista/presidencial', methods=['POST'])
def registrar_presidencial():
    data = request.get_json()
    resultado = registrar_lista_presidencial(data)
    if resultado == 'LISTA_NO_EXISTE':
        return jsonify({"error": "La lista base no existe"}), 400
    if resultado == 'YA_EXISTE_PRESIDENCIAL':
        return jsonify({"error": "La lista presidencial ya existe"}), 400
    if resultado == 'YA_EXISTE_OTRO_TIPO':
        return jsonify({"error": "La lista ya existe en otro tipo de elección"}), 400
    if resultado:
        return jsonify({"message": "Lista presidencial registrada"}), 201
    return jsonify({"error": "No se pudo registrar la lista presidencial"}), 500

@lista_bp.route('/lista/ballotage', methods=['POST'])
def registrar_ballotage():
    data = request.get_json()
    resultado = registrar_lista_ballotage(data)
    if resultado == 'LISTA_NO_EXISTE':
        return jsonify({"error": "La lista base no existe"}), 400
    if resultado == 'YA_EXISTE_BALLOTAGE':
        return jsonify({"error": "La lista ballotage ya existe"}), 400
    if resultado == 'YA_EXISTE_OTRO_TIPO':
        return jsonify({"error": "La lista ya existe en otro tipo de elección"}), 400
    if resultado == 'CANDIDATO_NO_EXISTE':
        return jsonify({"error": "El candidato especificado no existe"}), 400
    if resultado:
        return jsonify({"message": "Lista de ballotage registrada"}), 201
    return jsonify({"error": "No se pudo registrar la lista de ballotage"}), 500

@lista_bp.route('/lista/municipal', methods=['POST'])
def registrar_municipal():
    data = request.get_json()
    resultado = registrar_lista_municipal(data)
    if resultado == 'LISTA_NO_EXISTE':
        return jsonify({"error": "La lista base no existe"}), 400
    if resultado == 'YA_EXISTE_MUNICIPAL':
        return jsonify({"error": "La lista municipal ya existe"}), 400
    if resultado == 'YA_EXISTE_OTRO_TIPO':
        return jsonify({"error": "La lista ya existe en otro tipo de elección"}), 400
    if resultado == 'CANDIDATO_NO_EXISTE':
        return jsonify({"error": "El candidato especificado no existe"}), 400
    if resultado:
        return jsonify({"message": "Lista municipal registrada"}), 201
    return jsonify({"error": "No se pudo registrar la lista municipal"}), 500
