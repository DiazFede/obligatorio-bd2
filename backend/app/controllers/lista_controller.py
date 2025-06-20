from app.db import insert_data, get_one

def crear_lista(data):
    ya_existe = get_one("SELECT 1 FROM Lista WHERE id = %s", (data['id'],))
    if ya_existe:
        return 'YA_EXISTE'
    return insert_data("INSERT INTO Lista (id) VALUES (%s)", (data['id'],))

def agregar_papeleta(data):
    ya_existe = get_one("SELECT 1 FROM Papeleta WHERE id = %s", (data['id'],))
    if ya_existe:
        return 'YA_EXISTE'
    return insert_data("INSERT INTO Papeleta (id, opcion) VALUES (%s, %s)", (data['id'], data['opcion']))

def registrar_lista_presidencial(data):
    # Validar existencia lista base
    lista = get_one("SELECT 1 FROM Lista WHERE id = %s", (data['id'],))
    if not lista:
        return 'LISTA_NO_EXISTE'

    # Validar si ya existe lista presidencial con ese id
    ya_existe = get_one("SELECT 1 FROM Lista_Presidencial WHERE id = %s", (data['id'],))
    if ya_existe:
        return 'YA_EXISTE_PRESIDENCIAL'

    # Validar que no exista en otros tipos
    en_ballotage = get_one("SELECT 1 FROM Lista_Ballotage WHERE id = %s", (data['id'],))
    if en_ballotage:
        return 'YA_EXISTE_OTRO_TIPO'
    en_municipal = get_one("SELECT 1 FROM Lista_Municipal WHERE id = %s", (data['id'],))
    if en_municipal:
        return 'YA_EXISTE_OTRO_TIPO'

    query = "INSERT INTO Lista_Presidencial (id, presidente, vicepresidente, senadores, diputados) VALUES (%s, %s, %s, %s, %s)"
    params = (data['id'], data['presidente'], data['vicepresidente'], data['senadores'], data['diputados'])
    return insert_data(query, params)

def registrar_lista_ballotage(data):
    # Validar existencia lista base
    lista = get_one("SELECT 1 FROM Lista WHERE id = %s", (data['id'],))
    if not lista:
        return 'LISTA_NO_EXISTE'

    # Validar si ya existe lista ballotage con ese id
    ya_existe = get_one("SELECT 1 FROM Lista_Ballotage WHERE id = %s", (data['id'],))
    if ya_existe:
        return 'YA_EXISTE_BALLOTAGE'

    # Validar que no exista en otros tipos
    en_presidencial = get_one("SELECT 1 FROM Lista_Presidencial WHERE id = %s", (data['id'],))
    if en_presidencial:
        return 'YA_EXISTE_OTRO_TIPO'
    en_municipal = get_one("SELECT 1 FROM Lista_Municipal WHERE id = %s", (data['id'],))
    if en_municipal:
        return 'YA_EXISTE_OTRO_TIPO'

    # Validar candidato existente
    candidato = get_one("SELECT 1 FROM Candidato WHERE numero_credencial = %s OR nombre_partido = %s", (data['candidato'], data['candidato']))
    if not candidato:
        return 'CANDIDATO_NO_EXISTE'

    query = "INSERT INTO Lista_Ballotage (id, candidato) VALUES (%s, %s)"
    return insert_data(query, (data['id'], data['candidato']))

def registrar_lista_municipal(data):
    # Validar existencia lista base
    lista = get_one("SELECT 1 FROM Lista WHERE id = %s", (data['id'],))
    if not lista:
        return 'LISTA_NO_EXISTE'

    # Validar si ya existe lista municipal con ese id
    ya_existe = get_one("SELECT 1 FROM Lista_Municipal WHERE id = %s", (data['id'],))
    if ya_existe:
        return 'YA_EXISTE_MUNICIPAL'

    # Validar que no exista en otros tipos
    en_presidencial = get_one("SELECT 1 FROM Lista_Presidencial WHERE id = %s", (data['id'],))
    if en_presidencial:
        return 'YA_EXISTE_OTRO_TIPO'
    en_ballotage = get_one("SELECT 1 FROM Lista_Ballotage WHERE id = %s", (data['id'],))
    if en_ballotage:
        return 'YA_EXISTE_OTRO_TIPO'

    # Validar candidato existente
    candidato = get_one("SELECT 1 FROM Candidato WHERE numero_credencial = %s OR nombre_partido = %s", (data['candidato'], data['candidato']))
    if not candidato:
        return 'CANDIDATO_NO_EXISTE'

    query = "INSERT INTO Lista_Municipal (id, candidato) VALUES (%s, %s)"
    return insert_data(query, (data['id'], data['candidato']))
