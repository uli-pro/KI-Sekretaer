#!/usr/bin/env python
"""
ADHS-Assistent Flask Application Entry Point
"""
import os
from app import create_app

# App erstellen
app = create_app()

if __name__ == '__main__':
    # Development Server starten
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
