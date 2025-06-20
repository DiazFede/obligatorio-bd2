from app.db import get_one, get_all, insert_data, update_data, delete_data

def crear_comisaria(data):
    existe = get_one("SELECT 1 FROM Comisaria WHERE id = %s", (data['id'],))
    if existe:
        return 'YA_EXISTE'

    query = "INSERT INTO Comisaria (id, direccion) VALUES (%s, %s)"
    return insert_data(query, (data['id'], data['direccion']))

def obtener_comisarias():
    query = "SELECT * FROM Comisaria"
    return get_all(query)

def obtener_comisaria_por_id(id_comisaria):
    query = "SELECT * FROM Comisaria WHERE id = %s"
    return get_one(query, (id_comisaria,))

def actualizar_comisaria(id_comisaria, data):
    query = "UPDATE Comisaria SET direccion = %s WHERE id = %s"
    return update_data(query, (data['direccion'], id_comisaria))

def eliminar_comisaria(id_comisaria):
    query = "DELETE FROM Comisaria WHERE id = %s"
    return delete_data(query, (id_comisaria,))
