from app.db import insert_data, get_one

def registrar_acto_electoral(data):
    ciudadano = get_one("SELECT 1 FROM Ciudadano WHERE numero_credencial = %s", (data['numero_credencial'],))
    if not ciudadano:
        return 'CIUDADANO_NO_EXISTE'

    eleccion = get_one("SELECT 1 FROM Eleccion WHERE id_eleccion = %s", (data['id_eleccion'],))
    if not eleccion:
        return 'ELECCION_NO_EXISTE'

    ya_voto = get_one("SELECT 1 FROM Acto_Electoral WHERE numero_credencial = %s AND id_eleccion = %s", 
                      (data['numero_credencial'], data['id_eleccion']))
    if ya_voto:
        return 'YA_VOTO'

    query = "INSERT INTO Acto_Electoral (numero_credencial, id_eleccion) VALUES (%s, %s)"
    return insert_data(query, (data['numero_credencial'], data['id_eleccion']))
