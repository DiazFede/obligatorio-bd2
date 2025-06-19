import mysql.connector
from mysql.connector import Error
from app.config import Config # Importa la configuración de la base de datos

def get_db_connection():
    """Establece y retorna una conexión a la base de datos."""
    try:
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB
        )
        if connection.is_connected():
            print("Conexión a la base de datos MySQL exitosa.")
        return connection
    except Error as e:
        print(f"Error al conectar a la base de datos MySQL: {e}")
        return None

def close_db_connection(connection):
    """Cierra la conexión a la base de datos."""
    if connection and connection.is_connected():
        connection.close()
        print("Conexión a la base de datos MySQL cerrada.")

def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    """
    Ejecuta una consulta SQL.
    :param query: La cadena de la consulta SQL.
    :param params: Una tupla o diccionario de parámetros para la consulta.
    :param fetch_one: Si se debe retornar un solo resultado.
    :param fetch_all: Si se deben retornar todos los resultados.
    :return: Los resultados de la consulta, o None en caso de error.
    """
    connection = get_db_connection()
    result = None
    if connection:
        try:
            cursor = connection.cursor(dictionary=True) # dictionary=True para obtener resultados como diccionarios
            cursor.execute(query, params)
            if query.strip().upper().startswith(("INSERT", "UPDATE", "DELETE")):
                connection.commit()
                result = cursor.rowcount # Retorna el número de filas afectadas
            elif fetch_one:
                result = cursor.fetchone()
            elif fetch_all:
                result = cursor.fetchall()
            else:
                # Para SELECT sin fetch_one o fetch_all específicos, retornar todo por defecto
                result = cursor.fetchall()
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            connection.rollback() # Deshacer cambios en caso de error
        finally:
            cursor.close()
            close_db_connection(connection)
    return result

def get_one(query, params=None):
    """Ejecuta una consulta y retorna un solo resultado."""
    return execute_query(query, params, fetch_one=True)

def get_all(query, params=None):
    """Ejecuta una consulta y retorna todos los resultados."""
    return execute_query(query, params, fetch_all=True)

def insert_data(query, params=None):
    """Ejecuta una consulta INSERT y retorna el número de filas afectadas o el id del último insertado si aplica."""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
            if cursor.lastrowid: # Retorna el ID de la última fila insertada si la tabla tiene una clave primaria auto_increment
                return cursor.lastrowid
            return cursor.rowcount # O el número de filas afectadas para otras operaciones
        except Error as e:
            print(f"Error al insertar datos: {e}")
            connection.rollback()
            return None
        finally:
            cursor.close()
            close_db_connection(connection)
    return None

def update_data(query, params=None):
    """Ejecuta una consulta UPDATE."""
    return execute_query(query, params)

def delete_data(query, params=None):
    """Ejecuta una consulta DELETE."""
    return execute_query(query, params)