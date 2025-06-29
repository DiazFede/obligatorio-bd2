from app.db import insert_data, get_one, get_all

def crear_lista_municipal(data):
    lista = get_one("SELECT 1 FROM Lista WHERE id = %s", (data['id'],))
    if not lista:
        return 'LISTA_NO_EXISTE'

    ya_existe = get_one("SELECT 1 FROM Lista_Municipal WHERE id = %s", (data['id'],))
    if ya_existe:
        return 'YA_EXISTE'

    query = "INSERT INTO Lista_Municipal (id, candidato) VALUES (%s, %s)"
    return insert_data(query, (data['id'], data['candidato']))

def obtener_listas_municipales():
    return get_all("SELECT * FROM Lista NATURAL JOIN Lista_Municipal")
