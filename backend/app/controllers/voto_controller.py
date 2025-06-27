from app.db import insert_data, get_one
from datetime import date

def emitir_voto(data):
    id_lista = data.get("id_lista")
    numero_credencial = data.get("numero_credencial")
    id_eleccion = data.get("id_eleccion")

    # Verifica si el ciudadano ya emitió un voto en esta elección
    query_ya_voto = """
        SELECT 1
        FROM Acto_Electoral ae
        WHERE ae.numero_credencial = %s AND ae.id_eleccion = %s
    """
    ya_voto = get_one(query_ya_voto, (numero_credencial, id_eleccion))
    if ya_voto:
        return "YA_VOTO"

    # Registrar el voto (anónimo)
    query = """
        INSERT INTO Voto (id_lista, fecha, condicion)
        VALUES (%s, %s, %s)
    """
    return insert_data(query, (id_lista, date.today(), "emitido"))
