from app.db import get_one, get_all, insert_data, update_data, delete_data

def crear_establecimiento_eleccion(data):
    # Validar que el establecimiento exista
    establecimiento = get_one("SELECT 1 FROM Establecimiento WHERE numero_establecimiento = %s", (data['numero_establecimiento'],))
    if not establecimiento:
        return 'ESTABLECIMIENTO_NO_EXISTE'

    # Validar que la elección exista
    eleccion = get_one("SELECT 1 FROM Eleccion WHERE id_eleccion = %s", (data['id_eleccion'],))
    if not eleccion:
        return 'ELECCION_NO_EXISTE'

    # Validar que el circuito exista
    circuito = get_one("SELECT 1 FROM Circuito WHERE numero_circuito = %s", (data['numero_circuito'],))
    if not circuito:
        return 'CIRCUITO_NO_EXISTE'

    # Validar duplicado (PK compuesta)
    existe = get_one("""
        SELECT 1 FROM Establecimiento_Eleccion 
        WHERE numero_establecimiento = %s AND id_eleccion = %s AND numero_circuito = %s
    """, (data['numero_establecimiento'], data['id_eleccion'], data['numero_circuito']))
    if existe:
        return 'YA_EXISTE'

    query = """
        INSERT INTO Establecimiento_Eleccion (numero_establecimiento, id_eleccion, numero_circuito, credenciales_autorizadas)
        VALUES (%s, %s, %s, %s)
    """
    params = (
        data['numero_establecimiento'],
        data['id_eleccion'],
        data['numero_circuito'],
        data.get('credenciales_autorizadas', 0)  # Por defecto 0 si no se envía
    )
    return insert_data(query, params)

def obtener_establecimientos_eleccion():
    query = "SELECT * FROM Establecimiento_Eleccion"
    return get_all(query)

def eliminar_establecimiento_eleccion(numero_establecimiento, id_eleccion, numero_circuito):
    query = """
        DELETE FROM Establecimiento_Eleccion
        WHERE numero_establecimiento = %s AND id_eleccion = %s AND numero_circuito = %s
    """
    return delete_data(query, (numero_establecimiento, id_eleccion, numero_circuito))
