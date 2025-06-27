from app.db import insert_data, get_one, get_all

def crear_eleccion(data):
    query = """
        INSERT INTO Eleccion (id_eleccion, fecha, tipo)
        VALUES (%s, %s, %s)
    """
    params = (
        data.get('id_eleccion'),
        data.get('fecha'),
        data.get('tipo')
    )
    return insert_data(query, params)

def obtener_eleccion(id_eleccion):
    query = "SELECT * FROM Eleccion WHERE id_eleccion = %s"
    return get_one(query, (id_eleccion,))

from app.db import get_all

def obtener_todas_las_elecciones():
    query = "SELECT * FROM Eleccion"
    return get_all(query)


def elecciones_disponibles(numero_credencial):
    query = """
        SELECT e.*
        FROM Eleccion e
        JOIN Acto_Electoral ae ON ae.id_eleccion = e.id_eleccion
        WHERE ae.numero_credencial = %s
        AND ae.voto_emitido = 0
        AND e.status = TRUE
    """
    return get_all(query, (numero_credencial,))


def cambiar_estado_eleccion(id_eleccion, nuevo_estado):
    query = """
        UPDATE Eleccion
        SET status = %s
        WHERE id_eleccion = %s
    """
    return insert_data(query, (nuevo_estado, id_eleccion))