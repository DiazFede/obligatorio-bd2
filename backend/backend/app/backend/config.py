# backend/app/config.py

class Config:
    SECRET_KEY = 'tu_clave_secreta_super_segura' # Cambia esto por una clave real en producción
    MYSQL_HOST = 'localhost' # O la IP del servidor MySQL si Docker lo gestiona
    MYSQL_USER = 'root'      # Usuario de tu BD MySQL
    MYSQL_PASSWORD = 'tu_password_mysql' # Contraseña de tu BD MySQL
    MYSQL_DB = 'elecciones_db' # Nombre de tu base de datos