#  Implementierungsplan: KI-Sekretär (ADHS-Assistent)

## Executive Summary

Dieser Plan integriert die besten Erkenntnisse aus allen Analysen zu einem kohärenten, umsetzbaren Entwicklungsplan für Ihren KI-Sekretär. Der Fokus liegt auf Modul 1 (KI-Sekretär), mit vorbereitetem Fundament für Module 2+3.

## 1. Überarbeitete Datenbankarchitektur

### Skalierbare 3-Modul-Struktur (optimiert für alle Module)
```sql
-- Kernentitäten für alle Module
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    adhd_profile JSON, -- Energielevel, Präferenzen
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Erweiterte Task-Struktur für ADHS-spezifische Bedürfnisse
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    raw_input TEXT, -- Original-Nutzereingabe
    
    -- ADHS-optimierte Felder
    estimated_duration_min INTEGER,
    estimated_duration_max INTEGER,
    actual_duration INTEGER,
    energy_required INTEGER CHECK (energy_required IN (1,2,3)),
    emotional_weight INTEGER CHECK (emotional_weight IN (1,2,3,4,5)),
    
    -- Eisenhower-Matrix statt einfacher Priorität
    is_urgent BOOLEAN DEFAULT 0,
    is_important BOOLEAN DEFAULT 0,
    
    -- Status und Zeitverfolgung
    status TEXT DEFAULT 'pending' CHECK(status IN ('pending','in_progress','completed','deferred','cancelled')),
    deadline TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- KI-generierte Teilschritte (für Module 1+3)
CREATE TABLE task_steps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER NOT NULL,
    step_order INTEGER NOT NULL,
    description TEXT NOT NULL,
    estimated_minutes INTEGER,
    is_completed BOOLEAN DEFAULT 0,
    completed_at TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
);

-- Abhängigkeiten zwischen Aufgaben
CREATE TABLE task_dependencies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER NOT NULL,
    depends_on_task_id INTEGER NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
    FOREIGN KEY (depends_on_task_id) REFERENCES tasks(id) ON DELETE CASCADE
);

-- Vergebungsmechanismus - Aufgabenverlauf
CREATE TABLE task_deferrals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER NOT NULL,
    reason TEXT, -- "low_energy", "overwhelmed", "priorities_changed"
    new_deadline TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
);

-- Für Modul 2 (Planungsassistent) - vorbereitet
CREATE TABLE schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date DATE NOT NULL,
    energy_forecast INTEGER, -- 1-3 Skala
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Für Modul 3 (Fokus-Coach) - vorbereitet
CREATE TABLE focus_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    task_id INTEGER,
    planned_duration INTEGER NOT NULL,
    actual_duration INTEGER,
    interruptions INTEGER DEFAULT 0,
    quality_rating INTEGER, -- 1-5 Selbstbewertung
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (task_id) REFERENCES tasks(id)
);
```

## 2. Detaillierte 6-Wochen Entwicklungsroadmap

### Woche 1-2: Azure-optimiertes Fundament (15-20h)

**Tech-Stack Setup:**
- Flask + SQLite (Entwicklung) → PostgreSQL (Produktion)
- Azure OpenAI API (GPT-4) von Anfang an
- Vorbereitung für Azure App Service Deployment

**Deliverables:**
- [ ] Azure-Konto & OpenAI Service einrichten
- [ ] Flask-App mit Azure SDK konfigurieren
- [ ] Datenbank-Schema implementieren
- [ ] Basis-Authentifizierung (werkzeug.security)
- [ ] Erste Azure OpenAI Integration testen

**Code-Beispiel Kernstruktur:**
```python
# app.py - Azure-optimierte Basis
import os
from flask import Flask, render_template, request, jsonify
from openai import AzureOpenAI
import sqlite3

app = Flask(__name__)

# Azure OpenAI Konfiguration
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-02-15-preview"
)

@app.route('/api/secretary/parse', methods=['POST'])
def parse_task_input():
    user_input = request.json.get('input')
    
    # ADHS-optimierter System-Prompt
    system_prompt = """Du bist ein empathischer KI-Sekretär für Menschen mit ADHS. 
    Deine Aufgabe: Unstrukturierte Eingaben in klare, umsetzbare Aufgaben verwandeln.
    
    Extrahiere und strukturiere:
    1. Aufgabentitel (klar und motivierend formuliert)
    2. Benötigte Energie (1=niedrig, 2=mittel, 3=hoch)
    3. Geschätzte Dauer (realistisch, eher großzügig)
    4. Dringlichkeit und Wichtigkeit (Eisenhower-Matrix)
    5. Mögliche Teilschritte (max. 3-5 kleine Schritte)
    
    Bei fehlenden Infos: Stelle EINE präzise, hilfreiche Frage.
    Ton: Verständnisvoll, ermutigend, niemals wertend."""
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )
    
    return jsonify({"ai_response": response.choices[0].message.content})
```

### Woche 3-4: KI-Sekretär Kernfunktion (20-25h)

**ADHS-spezifische UX-Patterns:**
- Vergebende Sprache: "Lass uns das neu planen" statt "Überfällig"
- Energielevel-basierte Aufgabenvorschläge
- Ein-Klick-Verschiebung ohne Schuldgefühle

**Prompt-Engineering für ADHS:**
```python
def generate_task_breakdown_prompt(task_title, energy_level, user_context):
    return f"""
    Aufgabe: "{task_title}"
    Nutzer-Energielevel heute: {energy_level}/3
    
    Zerlege diese Aufgabe in 3-5 winzig kleine Schritte, die auch bei niedriger Energie machbar sind.
    Jeder Schritt sollte:
    - Maximal 15 Minuten dauern
    - Konkret und messbar sein
    - Einen kleinen Erfolg erzeugen
    
    Beispiel-Format:
    1. [2 Min] Arbeitsdokument öffnen und Titel eingeben
    2. [5 Min] Erste 3 Bullet Points skizzieren
    3. [10 Min] Punkt 1 ausformulieren
    
    Denk daran: Menschen mit ADHS brauchen schnelle Erfolge für Dopamin.
    """
```

**Deliverables:**
- [ ] Chat-Interface für Aufgabeneingabe
- [ ] KI-basierte Aufgabenzerlegung
- [ ] Intelligente Rückfragen-Logik
- [ ] Vergebungsmechanismus für verpasste Aufgaben
- [ ] ADHS-optimierte Taskansicht (nur das Nötigste)

### Woche 5-6: Frontend & ADHS-UX (15-20h)

**Emotionsaware UI-Komponenten:**
```css
/* ADHS-freundliche Farbpalette */
:root {
    --success-gentle: #22c55e;     /* Beruhigendes Grün */
    --warning-soft: #f59e0b;       /* Warmes Orange statt aggressives Rot */
    --focus-blue: #3b82f6;         /* Konzentrations-Blau */
    --energy-low: #64748b;         /* Gedämpftes Grau */
    --background-calm: #f8fafc;    /* Sehr helles, beruhigendes Grau */
}

.task-card {
    padding: 1rem;
    margin: 0.5rem 0;
    border-radius: 8px;
    transition: all 0.2s ease;
    border: 2px solid transparent;
}

.task-card.energy-match {
    border-color: var(--focus-blue);
    background: #eff6ff;
}

.forgiveness-button {
    background: var(--warning-soft);
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    font-size: 0.9rem;
}

.forgiveness-button:hover {
    background: #d97706;
    transform: scale(1.02);
}
```

**Adaptive Interface Logic:**
```javascript
// Energielevel-basierte UI-Anpassung
function adaptUIToEnergyLevel(energyLevel) {
    const taskList = document.getElementById('taskList');
    const taskCards = taskList.querySelectorAll('.task-card');
    
    taskCards.forEach(card => {
        const taskEnergy = parseInt(card.dataset.energyRequired);
        
        if (energyLevel === 1) { // Niedrige Energie
            if (taskEnergy > 1) {
                card.style.opacity = '0.3';
                card.classList.add('energy-mismatch');
            }
        } else if (energyLevel === 3) { // Hohe Energie
            if (taskEnergy === 3) {
                card.classList.add('energy-match');
            }
        }
    });
}

// Vergebungsvoller Umgang mit verpassten Aufgaben
function handleTaskMissed(taskId) {
    const reasons = [
        { id: 'low_energy', text: 'Hatte wenig Energie heute' },
        { id: 'overwhelmed', text: 'War überfördert' },
        { id: 'priorities_changed', text: 'Andere Prioritäten kamen dazwischen' }
    ];
    
    showReasonDialog(reasons, (reason) => {
        fetch('/api/tasks/defer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                task_id: taskId,
                reason: reason,
                message: 'Kein Problem! Wann sollen wir das nochmal versuchen?'
            })
        });
    });
}
```

## 3. KI-Integration: ADHS-optimierte Prompts

### Sekretär-Prompt-Bibliothek:

```python
PROMPTS = {
    'task_parsing': """
    Du bist ein KI-Sekretär für Menschen mit ADHS. Analysiere diese Eingabe:
    
    "{user_input}"
    
    Extrahiere:
    1. Was soll getan werden? (als motivierender Titel)
    2. Bis wann? (realistisch einschätzen)
    3. Wie aufwendig? (Min/Max Dauer)
    4. Wie wichtig/dringend? (Eisenhower-Matrix)
    5. Welche Energie braucht das? (1-3)
    
    Fehlende Infos: Stelle EINE präzise Frage.
    Format: JSON mit klarer Struktur.
    Ton: Verständnisvoll, ermutigend.
    """,
    
    'task_breakdown': """
    Zerlege "{task_title}" in 3-5 winzige Schritte für jemanden mit ADHS:
    
    Jeder Schritt:
    - Max 15 Minuten
    - Konkrete Aktion
    - Sofortiger kleiner Erfolg
    - Bei Energielevel {energy_level}/3 machbar
    
    Beginne mit dem allereinfachsten Schritt!
    """,
    
    'forgiveness_reframe': """
    Diese Aufgabe wurde verschoben: "{task_title}"
    Grund: {reason}
    
    Formuliere eine vergebende, motivierende Nachricht um.
    Vorschläge für nächste Schritte.
    Keine Schuldzuweisungen!
    """
}
```

## 4. Azure-Integration & Skalierungsarchitektur

### Produktionsreife von Tag 1:
```python
# config.py - Umgebungsbasierte Konfiguration
import os

class Config:
    # Azure OpenAI
    AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
    AZURE_OPENAI_KEY = os.getenv('AZURE_OPENAI_KEY')
    AZURE_OPENAI_DEPLOYMENT = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4')
    
    # Datenbank
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'sqlite:///adhs_assistant.db'
    
    # Sicherheit
    SECRET_KEY = os.getenv('SECRET_KEY') or 'dev-key-change-in-production'
    
    # DSGVO-Compliance
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev_adhs_assistant.db'

class ProductionConfig(Config):
    DEBUG = False
    # Azure PostgreSQL Connection String
    SQLALCHEMY_DATABASE_URI = os.getenv('AZURE_POSTGRESQL_CONNECTION')
```

## 5. ADHS-optimierte UX-Patterns

### Core-Designprinzipien:
1. **Vergebung vor Perfektion**: Niemand ist perfekt, das System auch nicht
2. **Energie-Awareness**: Aufgaben basierend auf aktueller Energie vorschlagen
3. **Minimale kognitive Last**: Nur das Nötigste zeigen
4. **Sofortige Erfolge**: Kleine Gewinne für Dopamin-Boost
5. **Flexibilität ohne Chaos**: Anpassbar, aber nicht überfordernd

### Konkrete UX-Implementierung:
```html
<!-- ADHS-optimiertes Task-Interface -->
<div class="task-input-container">
    <div class="energy-selector">
        <label>Wie fühlst du dich heute?</label>
        <div class="energy-buttons">
            <button class="energy-btn low" data-energy="1">🔋 Wenig Energie</button>
            <button class="energy-btn medium" data-energy="2">⚡ Geht so</button>
            <button class="energy-btn high" data-energy="3">🚀 Volle Power</button>
        </div>
    </div>
    
    <div class="task-input">
        <textarea placeholder="Was beschäftigt dich? Einfach reinschreiben..." 
                  id="taskInput" rows="3"></textarea>
        <button id="sendToSecretary" class="primary-btn">
            Lass uns das sortieren
        </button>
    </div>
</div>

<!-- Vergebungsvolle Task-Ansicht -->
<div class="task-card" data-energy-required="2">
    <div class="task-header">
        <h3>📧 E-Mail an Müller schreiben</h3>
        <span class="energy-indicator">⚡⚡</span>
    </div>
    
    <div class="task-meta">
        <span class="duration">15-30 Min</span>
        <span class="deadline calm">Bis morgen 10:00</span>
    </div>
    
    <div class="task-actions">
        <button class="action-btn start">Jetzt starten</button>
        <button class="action-btn defer gentle">Später machen</button>
        <button class="action-btn break-down">In Schritte zerlegen</button>
    </div>
</div>
```

## 6. Kritische Komponenten & Code-Beispiele

### Vergebungsmechanismus:
```python
@app.route('/api/tasks/defer', methods=['POST'])
def defer_task():
    data = request.get_json()
    task_id = data.get('task_id')
    reason = data.get('reason')
    
    # Aufgabe vergebungsvoll verschieben
    task = Task.query.get(task_id)
    
    # Kein "Überfällig" - nur sanfte Verschiebung
    new_deadline = datetime.now() + timedelta(days=1)
    task.deadline = new_deadline
    task.status = 'deferred'
    
    # Grund dokumentieren für Lernzwecke
    deferral = TaskDeferral(
        task_id=task_id,
        reason=reason,
        new_deadline=new_deadline
    )
    
    db.session.add(deferral)
    db.session.commit()
    
    return jsonify({
        "message": "Kein Problem! Manchmal läuft der Tag anders.",
        "new_deadline": new_deadline.isoformat(),
        "encouragement": "Morgen ist ein neuer Tag. Du schaffst das!"
    })
```

## 7. CS50-Erfolgskriterien Mapping

- ✅ **Funktionsfähige Web-App**: Flask + SQLite + Frontend
- ✅ **Komplexe Datenbankstruktur**: Relationale DB mit Foreign Keys
- ✅ **KI-Integration**: Azure OpenAI für intelligente Verarbeitung
- ✅ **JavaScript-Interaktivität**: Adaptive UI + AJAX
- ✅ **Reales Problem lösen**: ADHS-Unterstützung
- ✅ **Persönlicher Bezug**: Eigene ADHS-Erfahrung

## 8. Nächste Schritte & Priorisierung

### Sofort (diese Woche):
1. Azure-Konto einrichten + OpenAI Service aktivieren
2. Repository strukturieren (wie oben beschrieben)
3. Erste Flask-App mit Azure SDK testen

### Woche 1-2 Start:
1. Datenbank-Schema implementieren
2. Basis-Authentifizierung
3. Erste KI-Integration testen

### Entwicklungsphilosophie:
- **Mobile First**: Responsive Design von Anfang an
- **API First**: Alle Funktionen über APIs, Frontend als Consumer
- **Cloud Native**: Azure-Services optimal nutzen
- **ADHS-Driven Development**: Jede Entscheidung durch ADHS-Brille

Dieser Plan balanciert CS50-Anforderungen mit langfristiger Produktvision und integriert alle Insights aus den vorhandenen Analysen zu einem kohärenten, umsetzbaren Entwicklungsplan.