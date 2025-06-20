from app.db import insert_data, get_one

def registrar_ciudadano(data):
    query = """
        INSERT INTO Ciudadano (numero_credencial, CI, nombre, apellido, edad)
        VALUES (%s, %s, %s, %s, %s)
    """
    params = (
        data.get('numero_credencial'),
        data.get('CI'),
        data.get('nombre'),
        data.get('apellido'),
        data.get('edad')
    )
    return insert_data(query, params)

def obtener_ciudadano(credencial):
    query = "SELECT * FROM Ciudadano WHERE numero_credencial = %s"
    return get_one(query, (credencial,))
