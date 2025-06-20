from app.db import insert_data, get_one

def existe_ciudadano(numero_credencial):
    query = "SELECT 1 FROM Ciudadano WHERE numero_credencial = %s"
    return get_one(query, (numero_credencial,))

def existe_partido(nombre_partido):
    query = "SELECT 1 FROM Partido_politico WHERE nombre = %s"
    return get_one(query, (nombre_partido,))

def registrar_candidato(data):
    if not existe_ciudadano(data['numero_credencial']):
        return 'CIUDADANO_NO_EXISTE'
    if not existe_partido(data['nombre_partido']):
        return 'PARTIDO_NO_EXISTE'

    query = """
        INSERT INTO Candidato (numero_credencial, nombre_partido)
        VALUES (%s, %s)
    """
    params = (data['numero_credencial'], data['nombre_partido'])
    return insert_data(query, params)
