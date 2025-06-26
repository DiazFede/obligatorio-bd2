from app.db import get_all

def obtener_listas_presidenciales():
    return get_all("SELECT * FROM Lista NATURAL JOIN Lista_Presidencial")