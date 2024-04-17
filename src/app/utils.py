from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from functools import wraps

from app.models import Role, User

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        print(user.role_id)
        if user and user.role_id:
            role = Role.query.get(user.role_id)
            if role and role.name == "Administrator":
                return fn(*args, **kwargs)
            else:
                return jsonify({'error': 'Acceso restringido, se requiere rol de Administrador'}), 403
        else:
            return jsonify({'error': 'Usuario no válido'}), 401
    return wrapper