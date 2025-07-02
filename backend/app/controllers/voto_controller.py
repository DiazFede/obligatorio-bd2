from app.db import insert_data, get_one
from datetime import date

def emitir_voto(data):
    id_lista = data.get("id_lista")
    numero_credencial = data.get("numero_credencial")
    id_eleccion = data.get("id_eleccion")

    # Verificar que la elección esté abierta
    status_query = """
        SELECT tipo, fecha, status
        FROM Eleccion
        WHERE id_eleccion = %s
    """
    eleccion = get_one(status_query, (id_eleccion,))
    if not eleccion or not eleccion['status']:
        return "ELECCION_CERRADA"

    # Verificar habilitación y obtener circuito
    check_query = """
        SELECT voto_emitido, numero_circuito
        FROM Acto_Electoral
        WHERE numero_credencial = %s AND id_eleccion = %s
    """
    result = get_one(check_query, (numero_credencial, id_eleccion))

    if not result:
        return "NO_HABILITADO"

    if result['voto_emitido']:
        return "YA_VOTO"

    numero_circuito = result['numero_circuito']

    # Insertar el voto
    voto_query = """
        INSERT INTO Voto (id_lista, fecha, condicion, numero_circuito)
        VALUES (%s, %s, %s, %s)
    """
    insert_data(voto_query, (id_lista, date.today(), "emitido", numero_circuito))

    # Marcar que el ciudadano ya votó
    update_query = """
        UPDATE Acto_Electoral
        SET voto_emitido = TRUE
        WHERE numero_credencial = %s AND id_eleccion = %s
    """
    insert_data(update_query, (numero_credencial, id_eleccion))

    # Obtener datos del ciudadano para constancia
    ciudadano_query = """
        SELECT nombre, apellido, ci
        FROM Ciudadano
        WHERE numero_credencial = %s
    """
    ciudadano = get_one(ciudadano_query, (numero_credencial,))
    if not ciudadano:
        return "CIUDADANO_NO_EXISTE"

    return {
        "status": "OK",
        "ciudadano": {
            "nombre": ciudadano['nombre'],
            "apellido": ciudadano['apellido'],
            "ci": ciudadano['ci']
        },
        "eleccion": {
            "tipo": eleccion['tipo'],
            "fecha": eleccion['fecha'].strftime("%d/%m/%Y")
        }
    }
