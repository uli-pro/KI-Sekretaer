"""
User Model für ADHS-Assistent
"""
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import UUID
from app import db


class User(db.Model):
    """User Model mit Authentifizierung und Profil-Informationen"""
    
    __tablename__ = 'users'
    
    # Primary Key
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Authentication
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    username = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Profile
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    timezone = db.Column(db.String(50), default='Europe/Berlin')
    locale = db.Column(db.String(10), default='de_DE')
    
    # ADHS-spezifische Einstellungen (als JSON String in SQLite)
    energy_pattern = db.Column(db.Text)  # JSON: Tageszeitmuster für Energielevel
    adhd_preferences = db.Column(db.Text)  # JSON: ADHS-spezifische Einstellungen
    notification_settings = db.Column(db.Text)  # JSON: Benachrichtigungseinstellungen
    
    # Status
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    email_verified = db.Column(db.Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = db.Column(db.DateTime)
    
    # Relationships
    lebensbereiche = db.relationship('Lebensbereich', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    projekte = db.relationship('Projekt', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    aufgaben = db.relationship('Aufgabe', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    teilschritte = db.relationship('Teilschritt', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, email, username, password=None, **kwargs):
        """User initialisieren"""
        self.email = email.lower()
        self.username = username
        if password:
            self.set_password(password)
        super(User, self).__init__(**kwargs)
    
    def set_password(self, password):
        """Passwort hashen und speichern"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Passwort überprüfen"""
        return check_password_hash(self.password_hash, password)
    
    def update_last_login(self):
        """Last Login Timestamp aktualisieren"""
        self.last_login_at = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self, include_email=True):
        """User als Dictionary für API-Responses"""
        data = {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'timezone': self.timezone,
            'locale': self.locale,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login_at': self.last_login_at.isoformat() if self.last_login_at else None
        }
        
        if include_email:
            data['email'] = self.email
            data['email_verified'] = self.email_verified
        
        return data
    
    def __repr__(self):
        """String-Repräsentation"""
        return f'<User {self.username}>'
    
    # Validierungen
    @staticmethod
    def validate_email(email):
        """Email-Validierung"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_username(username):
        """Username-Validierung"""
        if len(username) < 3 or len(username) > 50:
            return False
        # Nur Buchstaben, Zahlen, Unterstrich und Bindestrich
        import re
        pattern = r'^[a-zA-Z0-9_-]+$'
        return re.match(pattern, username) is not None
    
    @classmethod
    def find_by_email(cls, email):
        """User by Email finden"""
        return cls.query.filter_by(email=email.lower()).first()
    
    @classmethod
    def find_by_username(cls, username):
        """User by Username finden"""
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def email_exists(cls, email):
        """Prüfen ob Email existiert"""
        return cls.query.filter_by(email=email.lower()).first() is not None
    
    @classmethod
    def username_exists(cls, username):
        """Prüfen ob Username existiert"""
        return cls.query.filter_by(username=username).first() is not None
