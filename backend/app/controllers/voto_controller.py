from app.db import insert_data, get_one
from datetime import date

def emitir_voto(data):
    id_lista = data.get("id_lista")
    numero_credencial = data.get("numero_credencial")
    id_eleccion = data.get("id_eleccion")

    status_query = """
        SELECT status
        FROM Eleccion
        WHERE id_eleccion = %s
    """
    status = get_one(status_query, (id_eleccion,))
    if not status or not status['status']:
        return "ELECCION_CERRADA"

    check_query = """
        SELECT voto_emitido
        FROM Acto_Electoral
        WHERE numero_credencial = %s AND id_eleccion = %s
    """
    result = get_one(check_query, (numero_credencial, id_eleccion))

    if not result:
        return "NO_HABILITADO"

    if result['voto_emitido']:
        return "YA_VOTO"

    voto_query = """
        INSERT INTO Voto (id_lista, fecha, condicion)
        VALUES (%s, %s, %s)
    """
    insert_data(voto_query, (id_lista, date.today(), "emitido"))

    update_query = """
        UPDATE Acto_Electoral
        SET voto_emitido = TRUE
        WHERE numero_credencial = %s AND id_eleccion = %s
    """
    insert_data(update_query, (numero_credencial, id_eleccion))

    return "OK"
