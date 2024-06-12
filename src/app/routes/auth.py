from flask import Blueprint, jsonify, request
from app.models import  User, db , Role
from flask_jwt_extended import create_access_token, jwt_required

auth_blueprint = Blueprint('auth', __name__)



@auth_blueprint.route('/register', methods=['POST'])
def register():
    email = request.json.get('email')
    password = request.json.get('password')
    role_id = 2
    
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'El correo ya existe'}), 409
    
    user = User(email=email, password=password, role_id=role_id)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'Usuario registrado con éxito'}), 201

@auth_blueprint.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    
    user = User.query.filter_by(email=email, password=password).first()
    if not user:
        return jsonify({'message': 'Credenciales inválidas'}), 401
    
    access_token = create_access_token(identity=user.id)
    role_data = {}
    if user.role_id:
        role = Role.query.filter_by(id=user.role_id).first()
        if role:
            role_data = role.to_dict()
    
    user_data = {
        'id': user.id,
        'email': user.email,
        'role': role_data,
        'access_token': access_token
    }        
    return jsonify(user_data), 200

@auth_blueprint.route('/users', methods=['GET'])
@jwt_required()  # Requiere autenticación para acceder a este endpoint
def get_users():
    # Realiza una consulta que incluye los roles. Usar 'join' es más eficiente si tienes configuradas las relaciones en SQLAlchemy.
    users = User.query.join(Role, User.role_id == Role.id).add_columns(User.id, User.email, Role.name).all()
    
    users_data = [{
        'id': user.User.id,  # Acceso a la columna de usuario
        'email': user.User.email,
        'role': user.name    # Acceso a la columna de nombre de rol
    } for user in users]  # Creación de una lista de diccionarios que incluyen el nombre del rol

    return jsonify(users_data), 200