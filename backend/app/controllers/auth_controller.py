from app.db import insert_data, get_one
from flask_jwt_extended import create_access_token
from datetime import timedelta
import re

def registrar_ciudadano(data):
    ci = re.sub(r'\D', '', data.get('CI', ''))

    existe = get_one("SELECT 1 FROM Ciudadano WHERE numero_credencial = %s", (data.get('numero_credencial'),))
    if existe:
        return None
    
    query = """
        INSERT INTO Ciudadano (numero_credencial, CI, nombre, apellido, edad)
        VALUES (%s, %s, %s, %s, %s)
    """
    params = (
        data.get('numero_credencial'),
        ci,
        data.get('nombre'),
        data.get('apellido'),
        data.get('edad')
    )
    return insert_data(query, params)

def login_ciudadano(data):
    ci = re.sub(r'\D', '', data.get('CI', ''))

    ciudadano = get_one("SELECT * FROM Ciudadano WHERE numero_credencial = %s AND CI = %s",
                        (data.get('numero_credencial'), ci))
    if not ciudadano:
        return None
    
    expires = timedelta(hours=2)
    access_token = create_access_token(identity=ciudadano['numero_credencial'], expires_delta=expires)
    
    return {
    "access_token": access_token,
    "numero_credencial": ciudadano['numero_credencial']
    }
