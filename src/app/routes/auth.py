from flask import Blueprint, jsonify, request
from app.models import  User, db
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
    return jsonify(access_token=access_token), 200