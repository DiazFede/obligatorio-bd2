from app.db import insert_data, get_one

def crear_partido(data):
    existe = get_one("SELECT 1 FROM Partido_politico WHERE nombre = %s", (data['nombre'],))
    if existe:
        return 'YA_EXISTE'

    query = """
        INSERT INTO Partido_politico (nombre, direccion_sede, presidente, vicepresidente)
        VALUES (%s, %s, %s, %s)
    """
    params = (
        data['nombre'],
        data['direccion_sede'],
        data['presidente'],
        data['vicepresidente']
    )
    return insert_data(query, params)
