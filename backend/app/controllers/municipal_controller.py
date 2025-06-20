from app.db import insert_data, get_one

def crear_lista_municipal(data):
    # Verificar si la lista base existe
    lista = get_one("SELECT 1 FROM Lista WHERE id = %s", (data['id'],))
    if not lista:
        return 'LISTA_NO_EXISTE'

    # Verificar si ya existe una lista municipal con ese ID
    ya_existe = get_one("SELECT 1 FROM Lista_Municipal WHERE id = %s", (data['id'],))
    if ya_existe:
        return 'YA_EXISTE'

    query = "INSERT INTO Lista_Municipal (id, candidato) VALUES (%s, %s)"
    return insert_data(query, (data['id'], data['candidato']))
