from app.db import get_one, get_all, insert_data, update_data, delete_data

def crear_agente(data):
    # Validar que no exista agente con ese número de placa
    existe = get_one("SELECT 1 FROM Agente_de_policia WHERE numero_placa = %s", (data['numero_placa'],))
    if existe:
        return 'YA_EXISTE'

    # Validar que exista el establecimiento
    establecimiento = get_one("SELECT 1 FROM Establecimiento WHERE numero_establecimiento = %s", (data['numero_establecimiento'],))
    if not establecimiento:
        return 'ESTABLECIMIENTO_NO_EXISTE'

    # Validar que exista la comisaría
    comisaria = get_one("SELECT 1 FROM Comisaria WHERE id = %s", (data['id_comisaria'],))
    if not comisaria:
        return 'COMISARIA_NO_EXISTE'

    query = """
        INSERT INTO Agente_de_policia (numero_placa, numero_establecimiento, id_comisaria)
        VALUES (%s, %s, %s)
    """
    params = (data['numero_placa'], data['numero_establecimiento'], data['id_comisaria'])
    return insert_data(query, params)

def obtener_agentes():
    query = """
        SELECT a.numero_placa, a.numero_establecimiento, a.id_comisaria,
               e.nombre AS nombre_establecimiento, c.direccion AS direccion_comisaria
        FROM Agente_de_policia a
        JOIN Establecimiento e ON a.numero_establecimiento = e.numero_establecimiento
        JOIN Comisaria c ON a.id_comisaria = c.id
    """
    return get_all(query)

def obtener_agente_por_placa(numero_placa):
    query = """
        SELECT numero_placa, numero_establecimiento, id_comisaria
        FROM Agente_de_policia
        WHERE numero_placa = %s
    """
    return get_one(query, (numero_placa,))

def actualizar_agente(numero_placa, data):
    # Validar que exista el establecimiento y comisaria si se modifican
    if 'numero_establecimiento' in data:
        establecimiento = get_one("SELECT 1 FROM Establecimiento WHERE numero_establecimiento = %s", (data['numero_establecimiento'],))
        if not establecimiento:
            return 'ESTABLECIMIENTO_NO_EXISTE'

    if 'id_comisaria' in data:
        comisaria = get_one("SELECT 1 FROM Comisaria WHERE id = %s", (data['id_comisaria'],))
        if not comisaria:
            return 'COMISARIA_NO_EXISTE'

    query = """
        UPDATE Agente_de_policia
        SET numero_establecimiento = %s, id_comisaria = %s
        WHERE numero_placa = %s
    """
    params = (data.get('numero_establecimiento'), data.get('id_comisaria'), numero_placa)
    return update_data(query, params)

def eliminar_agente(numero_placa):
    query = "DELETE FROM Agente_de_policia WHERE numero_placa = %s"
    return delete_data(query, (numero_placa,))
