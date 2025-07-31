"""
Konfiguration für die ADHS-Assistent App
"""
import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv

# Basis-Verzeichnis
BASE_DIR = Path(__file__).resolve().parent.parent

# .env Datei laden
load_dotenv(BASE_DIR / '.env')


class Config:
    """Basis-Konfiguration"""
    
    # Allgemeine Einstellungen
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = False
    TESTING = False
    
    # Datenbank
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        f'sqlite:///{BASE_DIR}/adhs_app.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # JWT Konfiguration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        seconds=int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_ALGORITHM = 'HS256'
    
    # CORS
    CORS_ORIGINS = os.environ.get(
        'CORS_ORIGINS',
        'http://localhost:3000,http://localhost:5173'
    ).split(',')
    
    # AI API Keys
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
    
    # Email (optional)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@adhs-app.com')
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'app.log')
    
    # File Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = BASE_DIR / 'uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'}
    
    # Feature Flags
    ENABLE_AI_FEATURES = os.environ.get('ENABLE_AI_FEATURES', 'true').lower() == 'true'
    ENABLE_EMAIL_NOTIFICATIONS = os.environ.get('ENABLE_EMAIL_NOTIFICATIONS', 'false').lower() == 'true'
    
    # Sicherheit
    BCRYPT_LOG_ROUNDS = int(os.environ.get('BCRYPT_LOG_ROUNDS', 12))
    
    # Session
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)


class DevelopmentConfig(Config):
    """Entwicklungs-Konfiguration"""
    DEBUG = True
    SQLALCHEMY_ECHO = True  # SQL-Queries loggen
    
    # Entwicklungs-spezifische Überschreibungen
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)  # Längere Token in Dev


class TestingConfig(Config):
    """Test-Konfiguration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-Memory DB für Tests
    WTF_CSRF_ENABLED = False
    
    # Schnellere Passwort-Hashes für Tests
    BCRYPT_LOG_ROUNDS = 4


class ProductionConfig(Config):
    """Produktions-Konfiguration"""
    DEBUG = False
    
    # Strikte Sicherheitseinstellungen
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # PostgreSQL in Produktion
    if os.environ.get('DATABASE_URL', '').startswith('postgres://'):
        # Heroku verwendet 'postgres://', SQLAlchemy braucht 'postgresql://'
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace(
            'postgres://', 'postgresql://', 1
        )


# Konfigurationen nach Umgebung
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Gibt die aktuelle Konfiguration basierend auf FLASK_ENV zurück"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])
