from flask import Blueprint, request, jsonify
from app.controllers.mesa_controller import crear_mesa
from app.controllers.mesa_controller import asignar_miembro
from app.db import get_all
from app.controllers.mesa_controller import obtener_mesa_por_ciudadano



mesa_bp = Blueprint('mesa', __name__)

@mesa_bp.route('/mesa/crear', methods=['POST'])
def crear():
    data = request.get_json()
    resultado = crear_mesa(data)
    if resultado == 'YA_EXISTE':
        return jsonify({"error": "La mesa ya existe"}), 400
    if resultado:
        return jsonify({"message": "Mesa creada correctamente"}), 201
    return jsonify({"error": "No se pudo crear la mesa"}), 500

@mesa_bp.route('/mesa/asignar_miembro', methods=['POST'])
def asignar_miembro_route():
    data = request.get_json()
    resultado = asignar_miembro(data)
    if resultado == 'CIUDADANO_NO_EXISTE':
        return jsonify({"error": "El ciudadano no existe"}), 400
    if resultado == 'MESA_NO_EXISTE':
        return jsonify({"error": "La mesa no existe"}), 400
    if resultado == 'MAXIMO_MIEMBROS':
        return jsonify({"error": "La mesa ya tiene 5 miembros asignados"}), 400
    if resultado == 'DUPLICADO_MISMO_MIEMBRO':
        return jsonify({"error": "El ciudadano ya está asignado a esta mesa"}), 400
    if resultado == 'ROL_YA_ASIGNADO':
        return jsonify({"error": "Ese rol ya está ocupado en esta mesa"}), 400
    if resultado:
        return jsonify({"message": "Miembro asignado correctamente"}), 201
    return jsonify({"error": "No se pudo asignar el miembro de mesa"}), 500


@mesa_bp.route('/mesa/miembros/<int:numero_mesa>', methods=['GET'])
def obtener_miembros_mesa(numero_mesa):
    query = """
        SELECT 
            mm.numero_credencial,
            c.nombre,
            c.apellido,
            mm.rol,
            mm.organismo_estatal
        FROM Miembro_de_mesa mm
        JOIN Ciudadano c ON mm.numero_credencial = c.numero_credencial
        WHERE mm.numero_mesa = %s
    """
    miembros = get_all(query, (numero_mesa,))
    if miembros:
        return jsonify(miembros), 200
    return jsonify({"message": "No se encontraron miembros asignados a esa mesa"}), 404

@mesa_bp.route('/mesa/ciudadano/<numero_credencial>', methods=['GET'])
def mesa_de_ciudadano(numero_credencial):
    resultado = obtener_mesa_por_ciudadano(numero_credencial)
    if resultado:
        return jsonify(resultado), 200
    return jsonify({"message": "El ciudadano no está asignado a ninguna mesa"}), 404
