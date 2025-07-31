# ADHS-Assistent (KI-Sekretär)

Ein KI-gestützter persönlicher Assistent für Menschen mit ADHS, der dabei hilft, komplexe Aufgaben in handhabbare Teilschritte zu zerlegen.

> Final Project für Harvard CS50

## 🎯 Projektziel

Der ADHS-Assistent unterstützt Nutzer dabei:
- Vage Eingaben wie "Geburtstag organisieren" in konkrete, ausführbare Aufgaben zu verwandeln
- Aufgaben in logische Teilschritte zu zerlegen
- Abhängigkeiten zwischen Aufgaben zu erkennen
- Den Überblick über verschiedene Lebensbereiche zu behalten
- Energie-Level und optimale Arbeitszeiten zu berücksichtigen

## 🚀 Features

### Kern-Funktionen
- **KI-gestützte Aufgabenzerlegung**: Automatische Erstellung von Teilschritten
- **Hierarchische Organisation**: Lebensbereiche → Projekte → Aufgaben → Teilschritte
- **Abhängigkeits-Management**: Erkennung und Visualisierung von Task-Abhängigkeiten
- **Multi-User-Fähigkeit**: Bis zu 5000 Nutzer unterstützt

### ADHS-spezifische Features
- **Energie-Level-Tracking**: Aufgaben nach benötigter Energie (1-3) kategorisieren
- **Prokrastinations-Warnung**: Erkennung von liegengebliebenen Aufgaben
- **Flexible Wiederholungen**: Unterstützung für wiederkehrende Aufgaben
- **Personen-Management**: Zuordnung von Personen und deren Rollen zu Aufgaben

## 🛠️ Technologie-Stack

### Backend
- **Python 3.11+** mit Flask
- **SQLAlchemy** ORM
- **SQLite** (Entwicklung) / **PostgreSQL** (Produktion)
- **JWT** für Authentifizierung
- **OpenAI/Anthropic API** für KI-Features

### Frontend (geplant)
- **React** oder **Vue.js**
- **Tailwind CSS** für Styling
- **Vite** als Build-Tool

## 📋 Voraussetzungen

- Python 3.11 oder höher
- pip (Python Package Manager)
- Git
- Virtualenv (empfohlen)
- OpenAI oder Anthropic API Key (für KI-Features)

## 🏃 Quick Start

### 1. Repository klonen
```bash
git clone https://github.com/dein-username/adhs-assistent.git
cd adhs-assistent
```

### 2. Virtuelle Umgebung erstellen
```bash
python3 -m venv .venv
source .venv/bin/activate  # Auf Windows: .venv\Scripts\activate
```

### 3. Dependencies installieren
```bash
make install-dev
# oder manuell:
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 4. Umgebungsvariablen konfigurieren
```bash
cp .env.example .env
# Bearbeite .env und füge deine API-Keys ein
```

### 5. Datenbank initialisieren
```bash
make db-init
make db-upgrade
```

### 6. Development Server starten
```bash
make dev
# oder: python -m flask run --debug
```

Die App läuft jetzt auf http://localhost:5000

## 📝 Verwendung

### API Endpoints (geplant)

```http
# Authentifizierung
POST   /api/auth/register
POST   /api/auth/login
POST   /api/auth/refresh

# Lebensbereiche
GET    /api/lebensbereiche
POST   /api/lebensbereiche
PUT    /api/lebensbereiche/:id
DELETE /api/lebensbereiche/:id

# Projekte
GET    /api/projekte
POST   /api/projekte
PUT    /api/projekte/:id
DELETE /api/projekte/:id

# KI-Features
POST   /api/ai/parse-task
POST   /api/ai/suggest-subtasks
```

## 🧪 Testing

```bash
# Alle Tests ausführen
make test

# Tests mit Coverage
pytest --cov=app --cov-report=html

# Tests im Watch-Modus
make test-watch
```

## 📚 Dokumentation

Weitere Dokumentation findest du im `docs/` Verzeichnis:
- [API-Dokumentation](docs/api/README.md)
- [Entwickler-Guide](docs/development/README.md)
- [Datenbank-Schema](docs/database-schema.md)

## 🤝 Beitragen

Contributions sind willkommen! Bitte lies [CONTRIBUTING.md](CONTRIBUTING.md) für Details.

### Development Workflow
1. Fork das Repository
2. Erstelle einen Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Committe deine Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. Push zum Branch (`git push origin feature/AmazingFeature`)
5. Öffne einen Pull Request

## 📄 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe [LICENSE](LICENSE) für Details.

## 👤 Autor

**Ulrich Probst**
- CS50 Final Project
- GitHub: [@dein-github-username]

## 🙏 Danksagungen

- Harvard CS50 Team für den großartigen Kurs
- OpenAI/Anthropic für die KI-APIs
- Die Open-Source-Community für die verwendeten Libraries

## 📈 Projekt-Status

🚧 **In aktiver Entwicklung** 🚧

Aktuelle Phase: Backend-Grundgerüst (siehe [Projektplan](docs/projektplan.md))

---

*Dies ist das Final Project für CS50. I am Ulrich Probst, and this is CS50!*
