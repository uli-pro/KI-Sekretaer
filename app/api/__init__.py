"""
API Blueprints
"""
from flask import Blueprint

# Blueprints erstellen
auth_bp = Blueprint('auth', __name__)
users_bp = Blueprint('users', __name__)
projects_bp = Blueprint('projects', __name__)

# Routes importieren (werden später erstellt)
# from . import auth, users, projects

__all__ = ['auth_bp', 'users_bp', 'projects_bp']
