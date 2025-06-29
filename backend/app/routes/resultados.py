from flask import Blueprint, request, jsonify
from app.db import update_data
from app.db import get_all, get_one
from app.controllers.resultados_controller import (
    obtener_resultados_circuito,
    obtener_resultados_agregados_partido_circuito,
    obtener_resultados_finales_candidato_circuito,
    obtener_resultados_departamento,
    obtener_ganador_departamento
)

resultados_bp = Blueprint('resultados', __name__)

@resultados_bp.route('/circuito/<int:id_circuito>/<int:id_eleccion>', methods=['GET'])
def get_circuito_results(id_circuito, id_eleccion):
    query_estado_circuito = "SELECT cerrado FROM Circuito_Estado WHERE numero_circuito = %s AND id_eleccion = %s"
    estado_circuito = get_one(query_estado_circuito, (id_circuito, id_eleccion))
    if not estado_circuito or not estado_circuito['cerrado']:
        return jsonify({"message": "La mesa de este circuito aún no está cerrada. Los resultados no están disponibles."}), 403

    resultados = obtener_resultados_circuito(id_circuito, id_eleccion)
    if resultados:
        return jsonify(resultados), 200
    return jsonify({"message": "No hay resultados para el circuito y elección especificados o un error ocurrió."}), 404

@resultados_bp.route('/circuito_agregado_partido/<int:id_circuito>/<int:id_eleccion>', methods=['GET'])
def get_circuito_agregado_partido_results(id_circuito, id_eleccion):
    query_estado_circuito = "SELECT cerrado FROM Circuito_Estado WHERE numero_circuito = %s AND id_eleccion = %s"
    estado_circuito = get_one(query_estado_circuito, (id_circuito, id_eleccion))
    if not estado_circuito or not estado_circuito['cerrado']:
        return jsonify({"message": "La mesa de este circuito aún no está cerrada. Los resultados no están disponibles."}), 403

    resultados = obtener_resultados_agregados_partido_circuito(id_circuito, id_eleccion)
    if resultados:
        return jsonify(resultados), 200
    return jsonify({"message": "No hay resultados agregados por partido para el circuito y elección especificados."}), 404

@resultados_bp.route('/circuito_final_candidato/<int:id_circuito>/<int:id_eleccion>', methods=['GET'])
def get_circuito_final_candidato_results(id_circuito, id_eleccion):
    query_estado_circuito = "SELECT cerrado FROM Circuito_Estado WHERE numero_circuito = %s AND id_eleccion = %s"
    estado_circuito = get_one(query_estado_circuito, (id_circuito, id_eleccion))
    if not estado_circuito or not estado_circuito['cerrado']:
        return jsonify({"message": "La mesa de este circuito aún no está cerrada. Los resultados no están disponibles."}), 403

    resultados = obtener_resultados_finales_candidato_circuito(id_circuito, id_eleccion)
    if resultados:
        return jsonify(resultados), 200
    return jsonify({"message": "No hay resultados finales por candidato para el circuito y elección especificados."}), 404

@resultados_bp.route('/departamento/<int:id_departamento>/<int:id_eleccion>', methods=['GET'])
def get_departamento_results(id_departamento, id_eleccion):
    resultados = obtener_resultados_departamento(id_departamento, id_eleccion)
    if resultados:
        return jsonify(resultados), 200
    return jsonify({"message": "No hay resultados para el departamento y elección especificados."}), 404

@resultados_bp.route('/departamento_ganador/<int:id_departamento>/<int:id_eleccion>', methods=['GET'])
def get_departamento_winner(id_departamento, id_eleccion):
    ganador = obtener_ganador_departamento(id_departamento, id_eleccion)
    if ganador:
        return jsonify(ganador), 200
    return jsonify({"message": "No se pudo determinar el ganador para el departamento y elección especificados, o los datos son insuficientes."}), 404


@resultados_bp.route('/cerrar_circuito/<int:id_circuito>/<int:id_eleccion>', methods=['POST'])
def cerrar_circuito(id_circuito, id_eleccion):
    query = "UPDATE Circuito_Estado SET cerrado = TRUE WHERE numero_circuito = %s AND id_eleccion = %s"
    resultado = update_data(query, (id_circuito, id_eleccion))
    if resultado:
        return jsonify({"message": "Circuito cerrado correctamente"}), 200
    return jsonify({"error": "No se pudo cerrar el circuito"}), 500
