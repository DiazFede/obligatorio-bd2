from app.db import insert_data, get_one
from datetime import date

def emitir_voto(data):
    id_lista = data.get("id_lista")
    numero_credencial = data.get("numero_credencial")
    id_eleccion = data.get("id_eleccion")

    # Verificar si ya emitió voto en esta elección
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

    # Insertar voto de forma anónima
    voto_query = """
        INSERT INTO Voto (id_lista, fecha, condicion)
        VALUES (%s, %s, %s)
    """
    insert_data(voto_query, (id_lista, date.today(), "emitido"))

    # Marcar que ya votó en Acto_Electoral
    update_query = """
        UPDATE Acto_Electoral
        SET voto_emitido = TRUE
        WHERE numero_credencial = %s AND id_eleccion = %s
    """
    insert_data(update_query, (numero_credencial, id_eleccion))

    return "OK"
