from app.db import get_one, get_all, insert_data, update_data, delete_data

def crear_departamento(data):
    existe = get_one("SELECT 1 FROM Departamento WHERE id = %s", (data['id'],))
    if existe:
        return 'YA_EXISTE'

    query = "INSERT INTO Departamento (id, nombre) VALUES (%s, %s)"
    return insert_data(query, (data['id'], data['nombre']))

def obtener_departamentos():
    query = "SELECT * FROM Departamento"
    return get_all(query)

def obtener_departamento_por_id(id_departamento):
    query = "SELECT * FROM Departamento WHERE id = %s"
    return get_one(query, (id_departamento,))

def actualizar_departamento(id_departamento, data):
    query = "UPDATE Departamento SET nombre = %s WHERE id = %s"
    return update_data(query, (data['nombre'], id_departamento))

def eliminar_departamento(id_departamento):
    query = "DELETE FROM Departamento WHERE id = %s"
    return delete_data(query, (id_departamento,))
