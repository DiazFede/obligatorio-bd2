from app.db import insert_data, get_one

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
