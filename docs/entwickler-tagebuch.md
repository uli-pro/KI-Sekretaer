# Entwickler-Tagebuch - ADHS-Assistent

## 📅 Stand: 31. Juli 2025

### 👤 Über Uli
- **Erfahrungslevel:** CS50 abgeschlossen, Anfänger
- **Verfügbare Zeit:** ~15 Stunden/Woche
- **Kenntnisse:** Python Basics, SQLite aus CS50, Git Grundlagen
- **Neue Technologien:** SQLAlchemy, Flask, JWT, API-Entwicklung

### 🎯 Angepasster Zeitplan
Mit 15 Stunden/Woche = **6-9 Monate** statt 13 Wochen

**Neue Zeitschätzung:**
- Phase 1 (Fundament): 4 Wochen statt 2
- Phase 2 (Backend-Kern): 6 Wochen statt 2
- Phase 3 (KI-Integration): 4 Wochen statt 2
- Weitere Phasen entsprechend angepasst

### 📍 Was wir heute gemacht haben

1. **Projektstruktur erstellt** ✅
   ```
   adhs-assistent/
   ├── app/           # Hauptcode
   ├── tests/         # Tests
   ├── docs/          # Dokumentation
   └── scripts/       # Hilfsskripte
   ```

2. **Wichtige Dateien angelegt** ✅
   - `.gitignore` - Git ignoriert unwichtige Dateien
   - `.env.example` - Vorlage für Umgebungsvariablen
   - `Makefile` - Shortcuts für häufige Commands
   - `requirements.txt` - Python-Pakete
   - `README.md` - Projektbeschreibung

3. **Flask-Grundgerüst** ✅
   - `app/__init__.py` - App-Factory
   - `app/config.py` - Konfiguration
   - `app/models/user.py` - Erstes Datenbank-Model

### 🔧 WICHTIG FÜR MORGEN - Was Uli als nächstes machen muss

#### Schritt 1: Terminal öffnen und zum Projekt navigieren
```bash
cd /Users/ulrichprobst/Library/Mobile\ Documents/com~apple~CloudDocs/1\ Uli\ Dokumente/A_Projekte/4\ Probst\ Dienstleistungen/Software-Entwicklung/harvard-cs50/adhs-assistent
```

#### Schritt 2: Virtuelle Umgebung erstellen
```bash
python3 -m venv .venv
```

#### Schritt 3: Virtuelle Umgebung aktivieren
```bash
source .venv/bin/activate
```
(Du siehst dann `(.venv)` vor deinem Terminal-Prompt)

#### Schritt 4: Git Status prüfen
```bash
git status
```

### 🗓️ Plan für die nächste Session

1. **Umgebung fertig einrichten** (30 Min)
   - Dependencies installieren
   - Prüfen ob alles läuft

2. **Erstes Model verstehen** (45 Min)
   - User-Model durchgehen
   - SQLAlchemy Basics lernen
   - Vergleich mit CS50 SQL

3. **Erste API Route** (45 Min)
   - Health-Check Endpoint
   - Postman/curl kennenlernen
   - Request/Response verstehen
