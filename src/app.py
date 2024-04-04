from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint

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


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/bd_crud'  
db = SQLAlchemy(app)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    permissions = db.Column(db.String(255), nullable=False)

    def __init__(self, name, description, permissions):
        self.name = name
        self.description = description
        self.permissions = permissions

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'permissions': self.permissions
        }

@app.route('/roles', methods=['GET'])
def get_roles():
    roles = Role.query.all()
    formatted_roles = [role.to_dict() for role in roles]
    return jsonify(formatted_roles)

@app.route('/roles/<int:role_id>', methods=['GET'])
def get_role(role_id):
    role = Role.query.get(role_id)
    if role:
        return jsonify(role.to_dict())
    else:
        return jsonify({'error': 'Rol no encontrado'}), 404

@app.route('/roles', methods=['POST'])
def create_role():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    permissions = data.get('permissions')

    if name and description and permissions:
        new_role = Role(name=name, description=description, permissions=permissions)
        db.session.add(new_role)
        db.session.commit()
        return jsonify({'message': 'Rol creado exitosamente'}), 201
    else:
        return jsonify({'error': 'Datos incompletos'}), 400

@app.route('/roles/<int:role_id>', methods=['PUT'])
def update_role(role_id):
    data = request.json
    role = Role.query.get(role_id)
    if role:
        role.name = data.get('name', role.name)
        role.description = data.get('description', role.description)
        role.permissions = data.get('permissions', role.permissions)
        db.session.commit()
        return jsonify({'message': 'Rol actualizado exitosamente'})
    else:
        return jsonify({'error': 'Rol no encontrado'}), 404

@app.route('/roles/<int:role_id>', methods=['DELETE'])
def delete_role(role_id):
    role = Role.query.get(role_id)
    if role:
        db.session.delete(role)
        db.session.commit()
        return jsonify({'message': 'Rol eliminado exitosamente'})
    else:
        return jsonify({'error': 'Rol no encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=4000)
