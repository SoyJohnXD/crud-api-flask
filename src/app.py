from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
import database as db

app = Flask(__name__)

SWAGGER_URL = '/docs'
API_URL = '/static/Swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Flask Crud"
    },
)

app.register_blueprint(swaggerui_blueprint)

@app.route('/swagger.json')
def swagger_json():
    swag = app.config.get("swagger")
    swag.update({"paths": app.config.get("paths")})
    return jsonify(swag)

# Función para formatear el rol como un objeto con claves específicas
def format_role(role):
    return {
        'id': role[0],
        'name': role[1],
        'description': role[2],
        'permissions': role[3]
    }

# Obtener todos los roles
@app.route('/roles', methods=['GET'])
def get_roles():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM rol")
    roles = cursor.fetchall()
    cursor.close()
    formatted_roles = [format_role(role) for role in roles]
    return jsonify(formatted_roles)

# Obtener un rol por su ID
@app.route('/roles/<int:role_id>', methods=['GET'])
def get_role(role_id):
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM rol WHERE id = %s", (role_id,))
    role = cursor.fetchone()
    cursor.close()
    if role:
        formatted_role = format_role(role)
        return jsonify(formatted_role)
    else:
        return jsonify({'error': 'Rol no encontrado'}), 404

# Crear un nuevo rol
@app.route('/roles', methods=['POST'])
def create_role():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    permissions = data.get('permissions')

    if name and description and permissions:
        cursor = db.database.cursor()
        sql = "INSERT INTO rol (name, description, permissions) VALUES (%s, %s, %s)"
        cursor.execute(sql, (name, description, permissions))
        db.database.commit()
        cursor.close()
        return jsonify({'message': 'Rol creado exitosamente'}), 201
    else:
        return jsonify({'error': 'Datos incompletos'}), 400

# Actualizar un rol existente
@app.route('/roles/<int:role_id>', methods=['PUT'])
def update_role(role_id):
    data = request.json
    name = data.get('name')
    description = data.get('description')
    permissions = data.get('permissions')

    if name and description and permissions:
        cursor = db.database.cursor()
        sql = "UPDATE rol SET name = %s, description = %s, permissions = %s WHERE id = %s"
        cursor.execute(sql, (name, description, permissions, role_id))
        db.database.commit()
        cursor.close()
        return jsonify({'message': 'Rol actualizado exitosamente'})
    else:
        return jsonify({'error': 'Datos incompletos'}), 400

# Eliminar un rol
@app.route('/roles/<int:role_id>', methods=['DELETE'])
def delete_role(role_id):
    cursor = db.database.cursor()
    cursor.execute("DELETE FROM rol WHERE id = %s", (role_id,))
    db.database.commit()
    cursor.close()
    return jsonify({'message': 'Rol eliminado exitosamente'})

if __name__ == '__main__':
    app.run(debug=True, port=4000)
