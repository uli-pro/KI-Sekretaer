# ADHS-Assistent Entwicklungsdokumentation

## Übersicht

Diese Dokumentation richtet sich an Entwickler, die am ADHS-Assistenten arbeiten oder das Projekt verstehen möchten.

## Inhalt

1. [Erste Schritte](#erste-schritte)
2. [Projektstruktur](#projektstruktur)
3. [Entwicklungsworkflow](#entwicklungsworkflow)
4. [Testing](#testing)
5. [Datenbank](#datenbank)
6. [API-Entwicklung](#api-entwicklung)
7. [KI-Integration](#ki-integration)

## Erste Schritte

### Entwicklungsumgebung einrichten

1. **Repository klonen**
   ```bash
   git clone <repository-url>
   cd adhs-assistent
   ```

2. **Virtuelle Umgebung erstellen**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # oder
   .venv\Scripts\activate  # Windows
   ```

3. **Dependencies installieren**
   ```bash
   make install-dev
   ```

4. **Umgebungsvariablen konfigurieren**
   ```bash
   cp .env.example .env
   # Bearbeite .env mit deinen Einstellungen
   ```

5. **Datenbank initialisieren**
   ```bash
   make db-init
   make db-upgrade
   ```

## Projektstruktur

```
adhs-assistent/
├── app/                # Hauptanwendung
│   ├── models/        # SQLAlchemy Models
│   ├── api/          # API Endpoints
│   ├── services/     # Business Logic
│   └── utils/        # Hilfsfunktionen
├── tests/            # Test Suite
├── docs/             # Dokumentation
└── scripts/          # Utility Scripts
```

## Entwicklungsworkflow

### Git Workflow

Wir verwenden Git Flow:

1. **Feature Branch erstellen**
   ```bash
   git checkout -b feature/deine-feature
   ```

2. **Änderungen committen** (Conventional Commits)
   ```bash
   git add .
   git commit -m "feat: Neue Funktion hinzugefügt"
   ```

3. **Push und Pull Request**
   ```bash
   git push origin feature/deine-feature
   ```

### Commit Message Format

- `feat:` Neue Feature
- `fix:` Bugfix
- `docs:` Dokumentation
- `style:` Formatierung
- `refactor:` Code-Refactoring
- `test:` Tests
- `chore:` Wartungsarbeiten

## Testing

### Tests ausführen

```bash
# Alle Tests
make test

# Mit Coverage
pytest --cov=app

# Bestimmte Test-Datei
pytest tests/unit/test_models.py

# Watch Mode
make test-watch
```

### Test-Struktur

```python
# tests/unit/test_user.py
import pytest
from app.models import User

class TestUser:
    def test_create_user(self, db):
        user = User(email="test@example.com")
        db.session.add(user)
        db.session.commit()
        assert user.id is not None
```

## Datenbank

### Migrationen

```bash
# Neue Migration erstellen
make db-migrate "Beschreibung der Änderung"

# Migration ausführen
make db-upgrade

# Migration rückgängig machen
make db-downgrade
```

### Models erstellen

```python
# app/models/example.py
from app import db
from datetime import datetime

class Example(db.Model):
    __tablename__ = 'examples'
    
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

## API-Entwicklung

### Neuen Endpoint erstellen

```python
# app/api/example.py
from flask import jsonify, request
from app.api import example_bp
from app.models import Example
from app import db

@example_bp.route('/', methods=['GET'])
def get_examples():
    examples = Example.query.all()
    return jsonify([e.to_dict() for e in examples])

@example_bp.route('/', methods=['POST'])
def create_example():
    data = request.get_json()
    example = Example(**data)
    db.session.add(example)
    db.session.commit()
    return jsonify(example.to_dict()), 201
```

### API-Dokumentation

Wir nutzen Swagger/OpenAPI für die API-Dokumentation:

```python
from flasgger import swag_from

@example_bp.route('/', methods=['GET'])
@swag_from('docs/get_examples.yml')
def get_examples():
    # ...
```

## KI-Integration

### OpenAI/Anthropic Setup

```python
# app/services/ai_service.py
import openai
from app.config import Config

class AIService:
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY
    
    def parse_task(self, user_input):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Du bist ein ADHS-Assistent..."},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content
```

## Best Practices

### Code-Stil

- Verwende Black für Formatierung
- Befolge PEP 8
- Schreibe Docstrings für alle Funktionen
- Type Hints verwenden wo möglich

### Sicherheit

- Niemals Secrets committen
- Input validieren
- SQL Injection durch ORM vermeiden
- CORS korrekt konfigurieren

### Performance

- Datenbankabfragen optimieren
- Caching wo sinnvoll
- Pagination für Listen
- Async Tasks für lange Operationen

## Debugging

### Flask Debug Mode

```bash
export FLASK_ENV=development
flask run --debug
```

### Python Debugger

```python
import pdb; pdb.set_trace()
# oder
import ipdb; ipdb.set_trace()  # besserer Debugger
```

### Logging

```python
from app.utils.logger import get_logger

logger = get_logger(__name__)
logger.info("Wichtige Information")
logger.error("Fehler aufgetreten", exc_info=True)
```

## Deployment

Siehe [Deployment Guide](deployment.md) für Produktions-Deployment.

## Hilfreiche Links

- [Flask Dokumentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Dokumentation](https://docs.sqlalchemy.org/)
- [pytest Dokumentation](https://docs.pytest.org/)
