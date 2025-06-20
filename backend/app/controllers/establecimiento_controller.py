from app.db import get_one, get_all, insert_data, update_data, delete_data

def crear_establecimiento(data):
    # Validar que la zona exista
    zona = get_one("SELECT 1 FROM Zona WHERE numero_zona = %s", (data['numero_zona'],))
    if not zona:
        return 'ZONA_NO_EXISTE'

    # Validar que no exista establecimiento con mismo número
    existe = get_one("SELECT 1 FROM Establecimiento WHERE numero_establecimiento = %s", (data['numero_establecimiento'],))
    if existe:
        return 'YA_EXISTE'

    query = """
        INSERT INTO Establecimiento (numero_establecimiento, nombre, direccion, tipo, numero_zona)
        VALUES (%s, %s, %s, %s, %s)
    """
    params = (
        data['numero_establecimiento'],
        data['nombre'],
        data['direccion'],
        data['tipo'],
        data['numero_zona']
    )
    return insert_data(query, params)

def obtener_establecimientos():
    query = "SELECT * FROM Establecimiento"
    return get_all(query)

def obtener_establecimiento_por_numero(numero_establecimiento):
    query = "SELECT * FROM Establecimiento WHERE numero_establecimiento = %s"
    return get_one(query, (numero_establecimiento,))

def actualizar_establecimiento(numero_establecimiento, data):
    zona = get_one("SELECT 1 FROM Zona WHERE numero_zona = %s", (data['numero_zona'],))
    if not zona:
        return 'ZONA_NO_EXISTE'

    query = """
        UPDATE Establecimiento
        SET nombre = %s, direccion = %s, tipo = %s, numero_zona = %s
        WHERE numero_establecimiento = %s
    """
    params = (data['nombre'], data['direccion'], data['tipo'], data['numero_zona'], numero_establecimiento)
    return update_data(query, params)

def eliminar_establecimiento(numero_establecimiento):
    # Aquí podrías agregar validaciones si el establecimiento está referenciado
    query = "DELETE FROM Establecimiento WHERE numero_establecimiento = %s"
    return delete_data(query, (numero_establecimiento,))
