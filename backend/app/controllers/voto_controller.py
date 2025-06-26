from app.db import insert_data, get_one
from datetime import date

def verificar_si_ya_voto(numero_credencial, id_eleccion):
    query = """
        SELECT * FROM Acto_Electoral
        WHERE numero_credencial = %s AND id_eleccion = %s
    """
    return get_one(query, (numero_credencial, id_eleccion))

def emitir_voto_completo(data):
    if circuito_esta_cerrado(data['numero_circuito']):
        return 'CIRCUITO_CERRADO'

    ya_voto = verificar_si_ya_voto(data['numero_credencial'], data['id_eleccion'])
    if ya_voto:
        return 'YA_VOTO'

    # Insert en Voto
    voto_query = """
        INSERT INTO Voto (id_voto, id_lista, fecha, condicion)
        VALUES (%s, %s, %s, %s)
    """
    voto_params = (
        data.get('id_voto'),
        data.get('id_lista'),
        data.get('fecha'),
        data.get('condicion')
    )
    voto_resultado = insert_data(voto_query, voto_params)

    # Insert en Acto_Electoral
    acto_query = """
        INSERT INTO Acto_Electoral (numero_credencial, id_eleccion)
        VALUES (%s, %s)
    """
    acto_params = (
        data.get('numero_credencial'),
        data.get('id_eleccion')
    )
    acto_resultado = insert_data(acto_query, acto_params)

    return voto_resultado and acto_resultado


def circuito_esta_cerrado(numero_circuito):
    query = "SELECT cerrado FROM Circuito WHERE numero_circuito = %s"
    resultado = get_one(query, (numero_circuito,))
    return resultado and resultado['cerrado'] == 1

def emitir_voto(data):
    id_lista = data.get("id_lista")
    numero_credencial = data.get("numero_credencial")

    query_eleccion = """
        SELECT ae.id_eleccion
        FROM Acto_Electoral ae
        JOIN Eleccion e ON ae.id_eleccion = e.id_eleccion
        WHERE ae.numero_credencial = %s
        AND NOT EXISTS (
            SELECT 1
            FROM Voto v
            JOIN Lista l ON l.id = v.id_lista
            WHERE l.id = %s
            AND v.fecha = CURRENT_DATE
        )
        LIMIT 1
    """
    eleccion = get_one(query_eleccion, (numero_credencial, id_lista))
    if not eleccion:
        return "YA_VOTO"

    query = """
        INSERT INTO Voto (id_lista, fecha, condicion)
        VALUES (%s, %s, %s)
    """
    return insert_data(query, (id_lista, date.today(), "emitido"))
