from app.db import insert_data, get_one, get_all

def crear_mesa(data):
    ya_existe = get_one("SELECT 1 FROM Mesa WHERE numero_mesa = %s", (data['numero_mesa'],))
    if ya_existe:
        return 'YA_EXISTE'

    query = "INSERT INTO Mesa (numero_mesa) VALUES (%s)"
    return insert_data(query, (data['numero_mesa'],))

def asignar_miembro(data):
    # Verificar que el ciudadano exista
    ciudadano = get_one("SELECT 1 FROM Ciudadano WHERE numero_credencial = %s", (data['numero_credencial'],))
    if not ciudadano:
        return 'CIUDADANO_NO_EXISTE'

    # Verificar que la mesa exista
    mesa = get_one("SELECT 1 FROM Mesa WHERE numero_mesa = %s", (data['numero_mesa'],))
    if not mesa:
        return 'MESA_NO_EXISTE'

    # Verificar si la persona ya está en la mesa
    ya_es_miembro = get_one("""
        SELECT 1 FROM Miembro_de_mesa
        WHERE numero_credencial = %s AND numero_mesa = %s
    """, (data['numero_credencial'], data['numero_mesa']))
    if ya_es_miembro:
        return 'DUPLICADO_MISMO_MIEMBRO'

    # Validar máximo de 5 miembros
    cantidad_actual = get_one("""
        SELECT COUNT(*) as cantidad FROM Miembro_de_mesa WHERE numero_mesa = %s
    """, (data['numero_mesa'],))['cantidad']
    if cantidad_actual >= 5:
        return 'MAXIMO_MIEMBROS'

    # Validar que roles clave no estén repetidos
    rol = data['rol']
    if rol in ['Presidente', 'Secretario', 'Vocal']:
        existe_rol = get_one("""
            SELECT 1 FROM Miembro_de_mesa
            WHERE numero_mesa = %s AND rol = %s
        """, (data['numero_mesa'], rol))
        if existe_rol:
            return 'ROL_YA_ASIGNADO'

    # Insertar miembro
    query = """
        INSERT INTO Miembro_de_mesa (numero_credencial, numero_mesa, rol, organismo_estatal)
        VALUES (%s, %s, %s, %s)
    """
    params = (
        data['numero_credencial'],
        data['numero_mesa'],
        rol,
        data['organismo_estatal']
    )
    return insert_data(query, params)

def obtener_mesa_por_ciudadano(numero_credencial):
    query = """
        SELECT numero_mesa, rol, organismo_estatal
        FROM Miembro_de_mesa
        WHERE numero_credencial = %s
    """
    return get_one(query, (numero_credencial,))