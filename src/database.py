# db.py
import mysql.connector

# Configuración de la base de datos
database = mysql.connector.connect(
    host='mysql-db',
    user='root',
    password='4444',
)

# Crear la base de datos si no existe
def create_database():
    cursor = database.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS bd_crud")
    cursor.close()

# Crear tablas
def create_tables():
    cursor = database.cursor()
    cursor.execute("USE bd_crud")
    cursor.execute("CREATE TABLE IF NOT EXISTS rol (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), description VARCHAR(255), permissions VARCHAR(255))")
    cursor.close()

# Insertar datos de prueba
def insert_test_data():
    cursor = database.cursor()
    cursor.execute("USE bd_crud")
    cursor.execute("INSERT INTO rol (name, description, permissions) VALUES ('Admin', 'Administrador del sistema', 'all')")
    cursor.execute("INSERT INTO rol (name, description, permissions) VALUES ('User', 'Usuario regular', 'read')")
    database.commit()
    cursor.close()

# Llamar a las funciones para crear la base de datos y los datos de prueba
create_database()
create_tables()
insert_test_data()
