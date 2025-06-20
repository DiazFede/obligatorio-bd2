from app.db import insert_data, get_one

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
