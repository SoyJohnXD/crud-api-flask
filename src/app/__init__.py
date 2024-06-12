from datetime import timedelta
from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from .extensions import db, jwt
from flask_mail import Mail


def create_app():
    app = Flask(__name__)
    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/bd_crud'
    app.config['JWT_SECRET_KEY'] = 'tu_super_secreto'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    
     # Configuración de Flask-Mail
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'testflask948@gmail.com' 
    app.config['MAIL_PASSWORD'] = 'Test5flask.'
    mail = Mail(app) 
    
    CORS(app)
    db.init_app(app)
    jwt.init_app(app)
    
    SWAGGER_URL = '/docs'  
    API_URL = '/static/swagger.json'
    swagger_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL, API_URL,
        config={'app_name': "Flask CRUD API"}
    )
    app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)

    from .routes.auth import auth_blueprint
    from .routes.role import role_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(role_blueprint)

    return app
