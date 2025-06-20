from app.db import get_one, get_all, insert_data, update_data, delete_data

def crear_zona(data):
    # Validar que el departamento exista
    departamento = get_one("SELECT 1 FROM Departamento WHERE id = %s", (data['id_departamento'],))
    if not departamento:
        return 'DEPARTAMENTO_NO_EXISTE'

    # Validar que no exista zona con ese número
    existe = get_one("SELECT 1 FROM Zona WHERE numero_zona = %s", (data['numero_zona'],))
    if existe:
        return 'YA_EXISTE'

    query = """
        INSERT INTO Zona (numero_zona, nombre, id_departamento)
        VALUES (%s, %s, %s)
    """
    params = (data['numero_zona'], data['nombre'], data['id_departamento'])
    return insert_data(query, params)

def obtener_zonas():
    query = "SELECT * FROM Zona"
    return get_all(query)

def obtener_zona_por_numero(numero_zona):
    query = "SELECT * FROM Zona WHERE numero_zona = %s"
    return get_one(query, (numero_zona,))

def actualizar_zona(numero_zona, data):
    departamento = get_one("SELECT 1 FROM Departamento WHERE id = %s", (data['id_departamento'],))
    if not departamento:
        return 'DEPARTAMENTO_NO_EXISTE'

    query = """
        UPDATE Zona
        SET nombre = %s, id_departamento = %s
        WHERE numero_zona = %s
    """
    params = (data['nombre'], data['id_departamento'], numero_zona)
    return update_data(query, params)

def eliminar_zona(numero_zona):
    # Aquí podrías validar que no haya establecimientos relacionados
    query = "DELETE FROM Zona WHERE numero_zona = %s"
    return delete_data(query, (numero_zona,))
