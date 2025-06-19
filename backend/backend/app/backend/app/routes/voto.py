# backend/app/routes/voto.py

from flask import Blueprint, request, jsonify
from app.db import get_one, insert_data, update_data
from datetime import datetime

voto_bp = Blueprint('voto', __name__)

# Simulación de un usuario logueado (en un sistema real, usarías Flask-Login o JWT)
# Para este ejemplo, el numero_credencial y el rol se pasarán en el body de la petición para simplificar
# En producción, esto vendría del token de sesión/autenticación.

@voto_bp.route('/emitir', methods=['POST'])
def emitir_voto():
    data = request.get_json()
    numero_credencial = data.get('numero_credencial')
    id_eleccion = data.get('id_eleccion')
    id_circuito = data.get('id_circuito')
    listas_elegidas = data.get('listas_elegidas', []) # Lista de IDs de listas/papeletas
    es_voto_en_blanco = data.get('es_voto_en_blanco', False)
    es_voto_anulado = data.get('es_voto_anulado', False)

    if not all([numero_credencial, id_eleccion, id_circuito]):
        return jsonify({"message": "Datos de voto incompletos."}), 400

    # 1. Verificar si el ciudadano ya votó en esta elección
    query_ya_voto = """
        SELECT COUNT(*) AS count FROM Acto_Electoral
        WHERE numero_credencial = %s AND id_eleccion = %s
    """
    ya_voto = get_one(query_ya_voto, (numero_credencial, id_eleccion))
    if ya_voto and ya_voto['count'] > 0:
        return jsonify({"message": "El ciudadano ya emitió su voto para esta elección."}), 403

    # 2. Verificar si el circuito existe y está abierto
    query_circuito = "SELECT * FROM Circuito WHERE numero_circuito = %s"
    circuito = get_one(query_circuito, (id_circuito,))
    if not circuito:
        return jsonify({"message": "Circuito no encontrado."}), 404

    # Verificar si el circuito está cerrado (asumimos un campo 'cerrado' en Circuito o una tabla de estado)
    query_estado_circuito = "SELECT cerrado FROM Circuito_Estado WHERE numero_circuito = %s AND id_eleccion = %s"
    estado_circuito = get_one(query_estado_circuito, (id_circuito, id_eleccion))
    if estado_circuito and estado_circuito['cerrado']:
        return jsonify({"message": "La mesa de este circuito está cerrada. No se pueden emitir más votos."}), 403

    # 3. Determinar si el voto es observado
    # Asumimos que hay una forma de saber el circuito autorizado del votante (ej. en Ciudadano o una tabla de padrón)
    query_padrón = "SELECT id_circuito_asignado FROM Ciudadano_Padron WHERE numero_credencial = %s AND id_eleccion = %s"
    padrón = get_one(query_padrón, (numero_credencial, id_eleccion))
    
    es_observado = False
    if padrón and padrón['id_circuito_asignado'] != id_circuito:
        es_observado = True # No votó donde le correspondía por padrón 

    # Determinar la condición del voto 
    condicion_voto = "Válido"
    if es_voto_en_blanco:
        condicion_voto = "En Blanco"
    elif es_voto_anulado:
        condicion_voto = "Anulado"
    elif es_observado:
        condicion_voto = "Observado" # O puedes tener "Observado-Válido", "Observado-Anulado", etc.


    # 4. Registrar el Acto Electoral (para saber que la persona votó) 
    query_acto_electoral = """
        INSERT INTO Acto_Electoral (numero_credencial, id_eleccion, fecha_hora_voto, es_observado, autorizado_presidente_mesa)
        VALUES (%s, %s, %s, %s, %s)
    """
    fecha_hora_voto = datetime.now()
    # Los votos observados deben ser autorizados por el presidente de mesa 
    # Por ahora, un voto observado no está "autorizado" hasta que el presidente lo marque
    acto_electoral_registrado = insert_data(query_acto_electoral,
                                           (numero_credencial, id_eleccion, fecha_hora_voto, es_observado, False if es_observado else True))

    if acto_electoral_registrado is None:
        return jsonify({"message": "Error al registrar el acto electoral."}), 500

    # 5. Registrar el Voto (sin vincular directamente al ciudadano) 
    query_voto = """
        INSERT INTO Voto (id_circuito, id_eleccion, fecha_hora_emision, condicion)
        VALUES (%s, %s, %s, %s)
    """
    id_voto = insert_data(query_voto, (id_circuito, id_eleccion, fecha_hora_voto, condicion_voto))

    if id_voto is None:
        # Si el voto no se registra, deberíamos considerar deshacer el acto electoral
        # Esto requeriría una transacción o una lógica de compensación
        return jsonify({"message": "Error al registrar el voto. Intente nuevamente."}), 500

    # 6. Vincular el voto con las listas/papeletas elegidas (si no es en blanco/anulado) 
    if not es_voto_en_blanco and not es_voto_anulado:
        for id_lista in listas_elegidas:
            query_voto_lista = """
                INSERT INTO Voto_Lista (id_voto, id_lista)
                VALUES (%s, %s)
            """
            insert_data(query_voto_lista, (id_voto, id_lista))

    # 7. Incrementar el contador de votos emitidos del circuito 
    query_incrementar_contador = """
        UPDATE Circuito_Estado
        SET votos_emitidos_count = votos_emitidos_count + 1
        WHERE numero_circuito = %s AND id_eleccion = %s
    """
    update_data(query_incrementar_contador, (id_circuito, id_eleccion))


    return jsonify({"message": "Voto emitido exitosamente.", "es_observado": es_observado, "condicion": condicion_voto}), 201

@voto_bp.route('/cerrar_mesa', methods=['POST'])
# En un sistema real, esto requeriría autenticación de "Presidente de Mesa"
def cerrar_mesa():
    data = request.get_json()
    numero_circuito = data.get('numero_circuito')
    id_eleccion = data.get('id_eleccion')
    
    if not all([numero_circuito, id_eleccion]):
        return jsonify({"message": "Número de circuito o ID de elección faltante."}), 400

    # Verificar si el usuario que llama es un presidente de mesa y está autorizado
    # (Lógica de autenticación/autorización aquí)
    user_role = data.get('user_role') # Solo para este ejemplo
    if user_role != 'presidente_mesa':
         return jsonify({"message": "No autorizado. Solo el presidente de mesa puede cerrar la mesa."}), 403

    # Marcar el circuito/mesa como cerrado para esta elección 
    query_cerrar_mesa = """
        UPDATE Circuito_Estado
        SET cerrado = TRUE
        WHERE numero_circuito = %s AND id_eleccion = %s AND cerrado = FALSE
    """
    rows_affected = update_data(query_cerrar_mesa, (numero_circuito, id_eleccion))

    if rows_affected > 0:
        return jsonify({"message": f"Mesa del circuito {numero_circuito} para la elección {id_eleccion} cerrada exitosamente."}), 200
    else:
        # Puede que ya estuviera cerrada o el circuito/elección no exista
        return jsonify({"message": "No se pudo cerrar la mesa o ya estaba cerrada."}), 400

@voto_bp.route('/autorizar_voto_observado', methods=['POST'])
def autorizar_voto_observado():
    data = request.get_json()
    numero_credencial = data.get('numero_credencial')
    id_eleccion = data.get('id_eleccion')

    if not all([numero_credencial, id_eleccion]):
        return jsonify({"message": "Datos incompletos para autorizar voto observado."}), 400

    # Verificar si el usuario que llama es un presidente de mesa
    user_role = data.get('user_role') # Solo para este ejemplo
    if user_role != 'presidente_mesa':
         return jsonify({"message": "No autorizado. Solo el presidente de mesa puede autorizar votos observados."}), 403

    # Actualizar el estado del acto electoral para marcar el voto observado como autorizado
    query_autorizar = """
        UPDATE Acto_Electoral
        SET autorizado_presidente_mesa = TRUE
        WHERE numero_credencial = %s AND id_eleccion = %s AND es_observado = TRUE AND autorizado_presidente_mesa = FALSE
    """
    rows_affected = update_data(query_autorizar, (numero_credencial, id_eleccion))

    if rows_affected > 0:
        return jsonify({"message": "Voto observado autorizado exitosamente."}), 200
    else:
        return jsonify({"message": "No se encontró un voto observado pendiente de autorización para el ciudadano y elección especificados."}), 404