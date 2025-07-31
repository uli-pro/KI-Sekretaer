"""
ADHS-Assistent Flask Application
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow

# Extensions initialisieren
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
jwt = JWTManager()
ma = Marshmallow()


def create_app(config_name=None):
    """Application Factory Pattern"""
    app = Flask(__name__)
    
    # Konfiguration laden
    if config_name is None:
        from .config import get_config
        app.config.from_object(get_config())
    else:
        from .config import config
        app.config.from_object(config[config_name])
    
    # Extensions initialisieren
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, origins=app.config['CORS_ORIGINS'])
    jwt.init_app(app)
    ma.init_app(app)
    
    # Blueprints registrieren
    from .api import auth_bp, users_bp, projects_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(projects_bp, url_prefix='/api/projects')
    
    # Error Handlers
    register_error_handlers(app)
    
    # Shell Context
    @app.shell_context_processor
    def make_shell_context():
        """Kontext für Flask Shell"""
        return {
            'db': db,
            'User': None,  # Wird später importiert
            'Lebensbereich': None,
            'Projekt': None,
            'Aufgabe': None,
            'Teilschritt': None
        }
    
    # Health Check Endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'service': 'ADHS-Assistent API'}, 200
    
    return app


def register_error_handlers(app):
    """Registriere Error Handler"""
    
    @app.errorhandler(404)
    def not_found_error(error):
        return {'error': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'error': 'Internal server error'}, 500
    
    @app.errorhandler(400)
    def bad_request_error(error):
        return {'error': 'Bad request'}, 400
    
    @app.errorhandler(401)
    def unauthorized_error(error):
        return {'error': 'Unauthorized'}, 401
    
    @app.errorhandler(403)
    def forbidden_error(error):
        return {'error': 'Forbidden'}, 403
