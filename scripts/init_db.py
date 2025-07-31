#!/usr/bin/env python3
"""
Initialisiere die Datenbank
"""
import sys
import os

# Füge den Parent-Directory zum Python-Path hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User


def init_database():
    """Initialisiere die Datenbank mit Tabellen"""
    app = create_app('development')
    
    with app.app_context():
        # Erstelle alle Tabellen
        db.create_all()
        print("✓ Datenbank-Tabellen erstellt")
        
        # Prüfe ob Admin-User existiert
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            # Erstelle Admin-User
            admin = User(
                email='admin@adhs-app.local',
                username='admin',
                password='admin123',  # Ändere das in Produktion!
                first_name='Admin',
                last_name='User',
                is_active=True,
                email_verified=True
            )
            
            try:
                admin.validate()
                db.session.add(admin)
                db.session.commit()
                print("✓ Admin-User erstellt (Username: admin, Passwort: admin123)")
            except Exception as e:
                print(f"✗ Fehler beim Erstellen des Admin-Users: {e}")
                db.session.rollback()
        else:
            print("✓ Admin-User existiert bereits")
        
        print("\nDatenbank-Initialisierung abgeschlossen!")
        print("Du kannst die App jetzt mit 'make dev' oder 'flask run' starten.")


if __name__ == '__main__':
    init_database()
