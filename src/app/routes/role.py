# role_routes.py
from flask import Blueprint, jsonify, request
from app.models import Role, User, db
from flask_jwt_extended import jwt_required
from flask_mail import Message

from app.utils import admin_required

role_blueprint = Blueprint('roles', __name__)

@role_blueprint.route('/roles', methods=['GET'])
@jwt_required()
@admin_required
def get_roles():
    roles = Role.query.all()
    formatted_roles = [role.to_dict() for role in roles]
    return jsonify(formatted_roles)

@role_blueprint.route('/roles/<int:role_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_role(role_id):
    role = Role.query.get(role_id)
    if role:
        return jsonify(role.to_dict())
    else:
        return jsonify({'error': 'Rol no encontrado'}), 404

@role_blueprint.route('/roles', methods=['POST'])
@jwt_required()
@admin_required
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

@role_blueprint.route('/roles/<int:role_id>', methods=['PUT'])
@jwt_required()
@admin_required
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

@role_blueprint.route('/roles/<int:role_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_role(role_id):
    role = Role.query.get(role_id)
    if role:
        db.session.delete(role)
        db.session.commit()
        return jsonify({'message': 'Rol eliminado exitosamente'})
    else:
        return jsonify({'error': 'Rol no encontrado'}), 404
    
@role_blueprint.route('/update_user_role/<int:user_id>/<int:role_id>', methods=['PUT'])
@jwt_required()
@admin_required
def assign_role_to_user(user_id, role_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    role = Role.query.get(role_id)
    if not role:
        return jsonify({'error': 'Rol no encontrado'}), 404

    user.role_id = role_id
    db.session.commit()

    """ # Enviar correo electrónico al usuario
    msg = Message("Actualización de Rol",
                  sender="admin@example.com",
                  recipients=[user.email])
    msg.body = f"Estimado/a {user.email}, tu rol ha sido actualizado a {role.name}. Descripción: {role.description}"
    mail.send(msg) """

    return jsonify({'message': f'Rol actualizado exitosamente y correo enviado a {user.email}'}), 200