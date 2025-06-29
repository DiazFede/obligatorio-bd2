from app.db import get_one

def verificar_admin(usuario, contrasena_plana):
    query = "SELECT contrasena FROM Admin WHERE usuario = %s"
    admin = get_one(query, (usuario,))
    if not admin:
        return False
    return contrasena_plana == admin['contrasena']
