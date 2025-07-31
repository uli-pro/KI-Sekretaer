# KI-Sekretär Entwicklungsplan - Phase 1

## Kritische Analyse der ChatGPT-Vorschläge

### Positive Aspekte
- Web-App Ansatz ist zukunftssicher
- Flask/Python nutzt bestehende CS50-Kenntnisse
- Text-vor-Sprache ist pragmatisch priorisiert
- LLM-Integration ist für echte ADHS-Unterstützung notwendig

### Verbesserungsbedarf
- Azure-Setup ist für CS50-Start zu komplex
- Externe Kalender-APIs sind Nice-to-have, nicht MVP
- Fehlende Fokussierung auf CS50-spezifische Erfolgskriterien
- Unterschätzt die Komplexität der ADHS-spezifischen UX

## Phase 1: CS50-MVP (40-50 Stunden)

**Ziel:** Funktionsfähiger Prototyp, der CS50-Anforderungen erfüllt

### Tech-Stack (pragmatisch)
- **Backend:** Flask + SQLite (nicht Azure - erst später)
- **Frontend:** Vanilla HTML/CSS/JS (kein komplexes Framework)
- **LLM:** OpenAI API (direkter Einstieg, später Azure-Migration)
- **Deployment:** Lokal für CS50, später Azure

### Kernfunktionen
1. **Unstrukturierte Eingabe:** "Muss noch Müller anrufen wegen Projekt"
2. **LLM-Verarbeitung:** Intelligente Extraktion + Rückfragen
3. **Strukturierte Speicherung:** In SQLite mit ADHS-optimierter Datenstruktur
4. **Aufgaben-Dashboard:** Einfache Listenansicht mit Prioritäten

## Detaillierte Wochenplanung

### Woche 1-2: Grundgerüst (15-20h)
**Deliverables:**
- [ ] Flask-App Setup mit SQLite
- [ ] Basis-Datenbankschema (Users, Tasks, Dependencies)
- [ ] Einfache User-Authentication
- [ ] OpenAI API Integration für Textverarbeitung
- [ ] Grundlegende HTML-Templates

**Datenbankschema (vereinfacht für CS50):**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    raw_input TEXT,
    status TEXT DEFAULT 'pending',
    priority INTEGER DEFAULT 3,
    energy_required INTEGER DEFAULT 2,
    estimated_duration INTEGER,
    deadline TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE task_dependencies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER NOT NULL,
    depends_on_task_id INTEGER NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(id),
    FOREIGN KEY (depends_on_task_id) REFERENCES tasks(id)
);
```

### Woche 3-4: Kernfunktion KI-Sekretär (15-20h)
**Deliverables:**
- [ ] Texteingabe-Interface mit Chat-ähnlicher UX
- [ ] LLM-Prompt-Engineering für ADHS-spezifische Extraktion
- [ ] Intelligente Rückfragen zur Vervollständigung
- [ ] Strukturierte Aufgaben-Erstellung in Datenbank
- [ ] ADHS-spezifische Felder (Energie-Level, Zeitschätzungen)

**LLM-Integration Beispiel:**
```python
def process_user_input(raw_text):
    prompt = f"""
    Analysiere diese ADHS-Nutzereingabe und extrahiere:
    1. Aufgabentitel
    2. Deadline (falls genannt)
    3. Geschätzte Dauer
    4. Abhängigkeiten
    5. Benötigte Energie (1-3)
    
    Eingabe: "{raw_text}"
    
    Falls Informationen fehlen, generiere max. 2 präzise Rückfragen.
    """
    # OpenAI API Call
    # Strukturierte Antwort verarbeiten
```

### Woche 5-6: Frontend & Polish (10-15h)
**Deliverables:**
- [ ] Dashboard mit Aufgaben-Übersicht
- [ ] Einfache Prioritäten-Visualisierung
- [ ] Responsive Design (Bootstrap)
- [ ] CS50-Dokumentation (README, Video)
- [ ] Testing und Debugging

## Besonderheiten dieses Ansatzes

### Warum dieser Plan besser ist
✅ **CS50-optimiert:** Fokus auf Code-Qualität statt Enterprise-Architektur  
✅ **Pragmatisch:** Bewährte Tools, minimale Komplexität  
✅ **ADHS-zentriert:** Berücksichtigt Fachexpertise im Zeitmanagement  
✅ **Zukunftssicher:** Einfache Migration zu Azure nach CS50  

### Risikominimierung
- Komplexe Infrastruktur erst nach bewiesenem Konzept
- Iterative Entwicklung mit funktionsfähigen Zwischenergebnissen
- Fokus auf CS50-Erfolgskriterien statt Produktfeatures

## Phase 2: Post-CS50 Migration (geplant)

### Azure-Migration (20-30h)
- Azure OpenAI Integration (Datenschutz)
- Azure App Service Deployment
- Erweiterte Authentifizierung

### ADHS-Optimierung
- Emotional-adaptive UI (basierend auf Energie-Level)
- "Vergebungsmechanismus" für verpasste Aufgaben
- Erste Kalender-Integration

### Vorbereitung für Module 2 & 3
- Erweiterte Datenbankstruktur
- API-Grundlagen für Planungsassistent
- Timer-Funktionalität für Fokuscoach

## Nächste Schritte

1. **Diese Woche:** Entwicklungsumgebung einrichten
2. **OpenAI Account:** API-Key besorgen (kostenlose Credits nutzen)
3. **Repository:** Git-Repository für Versionskontrolle anlegen
4. **Prototyping:** Mit einfachster Texteingabe beginnen

## Erfolgskriterien für CS50

- [ ] Funktionsfähige Web-App mit User-Login
- [ ] LLM-basierte Aufgabenverarbeitung
- [ ] Datenbank mit relationaler Struktur
- [ ] Frontend mit JavaScript-Interaktivität
- [ ] 3-Minuten-Demo-Video
- [ ] Umfassende README-Dokumentation

*Dieser Plan balanciert CS50-Anforderungen mit langfristiger Produktvision und nutzt Ihre ADHS-Expertise optimal.*