# SQLite3-kompatibles ADHS-App Schema

## Anpassungen für SQLite3

Dieses Schema ist eine vereinfachte Version des ursprünglichen PostgreSQL-Schemas, angepasst für SQLite3-Kompatibilität.

### Hauptänderungen:
- UUID → TEXT (mit generierten IDs in der Anwendung)
- JSON → TEXT (JSON-Strings speichern)
- Arrays → Separate Tabellen oder kommaseparierte Strings
- Keine Stored Procedures → Anwendungslogik
- Vereinfachte Constraints

## Kern-Tabellen

### 1. users
```sql
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL CHECK (email LIKE '%@%.%'),
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    first_name TEXT,
    last_name TEXT,
    timezone TEXT DEFAULT 'Europe/Berlin',
    locale TEXT DEFAULT 'de_DE',
    energy_pattern TEXT, -- JSON als String
    adhd_preferences TEXT, -- JSON als String
    notification_settings TEXT, -- JSON als String
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login_at DATETIME,
    is_active INTEGER DEFAULT 1 CHECK (is_active IN (0, 1)),
    email_verified INTEGER DEFAULT 0 CHECK (email_verified IN (0, 1))
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_active ON users(is_active) WHERE is_active = 1;
```

### 2. lebensbereiche
```sql
CREATE TABLE lebensbereiche (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    name TEXT NOT NULL,
    beschreibung TEXT,
    farbe TEXT DEFAULT '#808080' CHECK (farbe GLOB '#[0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f][0-9A-Fa-f]'),
    prioritaet INTEGER CHECK (prioritaet BETWEEN 1 AND 5),
    woechentlich_verfuegbare_zeit INTEGER, -- in Minuten
    bevorzugte_tageszeiten TEXT, -- JSON als String
    is_active INTEGER DEFAULT 1 CHECK (is_active IN (0, 1)),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(user_id, name)
);

CREATE INDEX idx_lebensbereiche_user ON lebensbereiche(user_id);
CREATE INDEX idx_lebensbereiche_active ON lebensbereiche(user_id, is_active) WHERE is_active = 1;
```

### 3. projekte
```sql
CREATE TABLE projekte (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    lebensbereich_id TEXT NOT NULL,
    name TEXT NOT NULL,
    beschreibung TEXT,
    farbe TEXT DEFAULT '#808080',
    ist_wichtig INTEGER DEFAULT 0 CHECK (ist_wichtig IN (0, 1)),
    ist_dringend INTEGER DEFAULT 0 CHECK (ist_dringend IN (0, 1)),
    status TEXT NOT NULL DEFAULT 'offen' CHECK (status IN ('offen', 'begonnen', 'verschoben', 'abgeschlossen', 'abgebrochen')),
    aufwand_geschaetzt_min INTEGER,
    aufwand_geschaetzt_max INTEGER,
    aufwand_tatsaechlich INTEGER,
    deadline DATE,
    startdatum DATE,
    is_active INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (lebensbereich_id) REFERENCES lebensbereiche(id) ON DELETE CASCADE,
    CHECK (aufwand_geschaetzt_min <= aufwand_geschaetzt_max)
);

CREATE INDEX idx_projekte_user ON projekte(user_id);
CREATE INDEX idx_projekte_lebensbereich ON projekte(lebensbereich_id);
CREATE INDEX idx_projekte_status ON projekte(user_id, status);
CREATE INDEX idx_projekte_deadline ON projekte(deadline) WHERE deadline IS NOT NULL;
```

### 4. aufgaben
```sql
CREATE TABLE aufgaben (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    projekt_id TEXT NOT NULL,
    name TEXT NOT NULL,
    beschreibung TEXT,
    farbe TEXT DEFAULT '#808080',
    benoetigtes_energie_level INTEGER CHECK (benoetigtes_energie_level BETWEEN 1 AND 3),
    ist_wichtig INTEGER DEFAULT 0,
    ist_dringend INTEGER DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'offen',
    aufwand_geschaetzt_min INTEGER,
    aufwand_geschaetzt_max INTEGER,
    aufwand_tatsaechlich INTEGER,
    deadline DATETIME,
    startdatum DATE,
    is_active INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (projekt_id) REFERENCES projekte(id) ON DELETE CASCADE
);

CREATE INDEX idx_aufgaben_user ON aufgaben(user_id);
CREATE INDEX idx_aufgaben_projekt ON aufgaben(projekt_id);
CREATE INDEX idx_aufgaben_status ON aufgaben(user_id, status);
CREATE INDEX idx_aufgaben_energie ON aufgaben(benoetigtes_energie_level);
```

### 5. teilschritte
```sql
CREATE TABLE teilschritte (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    aufgabe_id TEXT NOT NULL,
    name TEXT NOT NULL,
    beschreibung TEXT,
    farbe TEXT DEFAULT '#808080',
    reihenfolge_nummer INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'offen',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (aufgabe_id) REFERENCES aufgaben(id) ON DELETE CASCADE,
    UNIQUE(aufgabe_id, reihenfolge_nummer)
);

CREATE INDEX idx_teilschritte_user ON teilschritte(user_id);
CREATE INDEX idx_teilschritte_aufgabe ON teilschritte(aufgabe_id);
```

### 6. personen
```sql
CREATE TABLE personen (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    vorname TEXT,
    nachname TEXT,
    anzeigename TEXT NOT NULL,
    email TEXT CHECK (email IS NULL OR email LIKE '%@%.%'),
    telefon TEXT,
    notizen TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_personen_user ON personen(user_id);
```

### 7. rollen
```sql
CREATE TABLE rollen (
    id TEXT PRIMARY KEY,
    user_id TEXT, -- NULL für System-Rollen
    name TEXT NOT NULL,
    beschreibung TEXT,
    is_system_rolle INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- System-Rollen einfügen
INSERT INTO rollen (id, name, beschreibung, is_system_rolle) VALUES
    ('role_1', 'Auftraggeber', 'Person, die eine Aufgabe in Auftrag gibt', 1),
    ('role_2', 'Ausführender', 'Person, die eine Aufgabe ausführt', 1),
    ('role_3', 'Berater', 'Person, die beratend zur Seite steht', 1),
    ('role_4', 'Prüfer', 'Person, die Ergebnisse prüft', 1),
    ('role_5', 'Informant', 'Person, die Informationen bereitstellt', 1);
```

### 8. personen_zuordnungen
```sql
CREATE TABLE personen_zuordnungen (
    id TEXT PRIMARY KEY,
    person_id TEXT NOT NULL,
    rolle_id TEXT NOT NULL,
    entity_type TEXT NOT NULL CHECK (entity_type IN ('lebensbereich', 'projekt', 'aufgabe', 'teilschritt')),
    entity_id TEXT NOT NULL,
    notizen TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (person_id) REFERENCES personen(id) ON DELETE CASCADE,
    FOREIGN KEY (rolle_id) REFERENCES rollen(id) ON DELETE CASCADE
);

CREATE INDEX idx_personen_zuord_person ON personen_zuordnungen(person_id);
CREATE INDEX idx_personen_zuord_entity ON personen_zuordnungen(entity_type, entity_id);
```

### 9. tags
```sql
CREATE TABLE tags (
    id TEXT PRIMARY KEY,
    user_id TEXT, -- NULL für System-Tags
    name TEXT NOT NULL,
    farbe TEXT DEFAULT '#808080',
    kategorie TEXT,
    is_system_tag INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(user_id, name)
);

-- Beispiel-System-Tags
INSERT INTO tags (id, name, kategorie, farbe, is_system_tag) VALUES
    ('tag_1', 'Schnell erledigt', 'Zeit', '#00FF00', 1),
    ('tag_2', 'Kreativ', 'Art', '#FF00FF', 1),
    ('tag_3', 'Routine', 'Art', '#0000FF', 1),
    ('tag_4', 'Kommunikation', 'Art', '#FFFF00', 1),
    ('tag_5', 'Konzentration', 'Energie', '#FF0000', 1),
    ('tag_6', 'Bewegung', 'Art', '#00FFFF', 1);
```

### 10. tag_zuordnungen
```sql
CREATE TABLE tag_zuordnungen (
    id TEXT PRIMARY KEY,
    tag_id TEXT NOT NULL,
    entity_type TEXT NOT NULL CHECK (entity_type IN ('projekt', 'aufgabe')),
    entity_id TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE,
    UNIQUE(tag_id, entity_type, entity_id)
);

CREATE INDEX idx_tag_zuord_tag ON tag_zuordnungen(tag_id);
CREATE INDEX idx_tag_zuord_entity ON tag_zuordnungen(entity_type, entity_id);
```

### 11. abhaengigkeiten
```sql
CREATE TABLE abhaengigkeiten (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    abhaengig_type TEXT NOT NULL CHECK (abhaengig_type IN ('projekt', 'aufgabe', 'teilschritt')),
    abhaengig_id TEXT NOT NULL,
    voraussetzung_type TEXT NOT NULL CHECK (voraussetzung_type IN ('projekt', 'aufgabe', 'teilschritt')),
    voraussetzung_id TEXT NOT NULL,
    beschreibung TEXT,
    is_blocking INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CHECK (NOT (abhaengig_type = voraussetzung_type AND abhaengig_id = voraussetzung_id)),
    UNIQUE(abhaengig_type, abhaengig_id, voraussetzung_type, voraussetzung_id)
);

CREATE INDEX idx_abhaeng_user ON abhaengigkeiten(user_id);
CREATE INDEX idx_abhaeng_abhaengig ON abhaengigkeiten(abhaengig_type, abhaengig_id);
CREATE INDEX idx_abhaeng_voraussetzung ON abhaengigkeiten(voraussetzung_type, voraussetzung_id);
```

### 12. arbeits_logs
```sql
CREATE TABLE arbeits_logs (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    entity_type TEXT NOT NULL CHECK (entity_type IN ('projekt', 'aufgabe', 'teilschritt')),
    entity_id TEXT NOT NULL,
    aktion TEXT NOT NULL CHECK (aktion IN ('angelegt', 'begonnen', 'bearbeitet', 'pausiert', 'fortgesetzt', 'abgeschlossen', 'abgebrochen')),
    start_zeit DATETIME NOT NULL,
    end_zeit DATETIME,
    dauer_minuten INTEGER, -- Muss in der Anwendung berechnet werden
    energie_level INTEGER CHECK (energie_level BETWEEN 1 AND 3),
    notizen TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CHECK (end_zeit IS NULL OR end_zeit > start_zeit)
);

CREATE INDEX idx_logs_user ON arbeits_logs(user_id);
CREATE INDEX idx_logs_entity ON arbeits_logs(entity_type, entity_id);
CREATE INDEX idx_logs_zeit ON arbeits_logs(user_id, start_zeit);
CREATE INDEX idx_logs_active ON arbeits_logs(user_id, end_zeit) WHERE end_zeit IS NULL;
```

### 13. wiederholungsmuster
```sql
CREATE TABLE wiederholungsmuster (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    name TEXT,
    muster_typ TEXT NOT NULL CHECK (muster_typ IN ('stündlich', 'täglich', 'wochentage', 'wöchentlich', 'monatstage', 'monatlich', 'jährlich')),
    konfiguration TEXT NOT NULL, -- JSON als String
    start_datum DATE NOT NULL,
    end_datum DATE,
    naechste_ausfuehrung DATETIME,
    is_active INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_wiederholung_user ON wiederholungsmuster(user_id);
CREATE INDEX idx_wiederholung_next ON wiederholungsmuster(naechste_ausfuehrung) WHERE is_active = 1;
```

### 14. user_eingaben_raw
```sql
-- Da SQLite keine Arrays unterstützt, separate Tabelle für unverarbeitete Eingaben
CREATE TABLE user_eingaben_raw (
    id TEXT PRIMARY KEY,
    entity_type TEXT NOT NULL CHECK (entity_type IN ('lebensbereich', 'projekt', 'aufgabe')),
    entity_id TEXT NOT NULL,
    eingabe_text TEXT NOT NULL,
    verarbeitet INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_eingaben_entity ON user_eingaben_raw(entity_type, entity_id);
```

## Trigger für automatische Updates

### Updated_at Trigger
```sql
-- Trigger für users
CREATE TRIGGER update_users_updated_at 
AFTER UPDATE ON users
FOR EACH ROW
WHEN NEW.updated_at = OLD.updated_at
BEGIN
    UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Trigger für lebensbereiche
CREATE TRIGGER update_lebensbereiche_updated_at 
AFTER UPDATE ON lebensbereiche
FOR EACH ROW
WHEN NEW.updated_at = OLD.updated_at
BEGIN
    UPDATE lebensbereiche SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Weitere Trigger für andere Tabellen nach gleichem Muster...
```

### Dauer-Berechnung Trigger
```sql
-- Trigger für arbeits_logs Dauer-Berechnung
CREATE TRIGGER calculate_duration
AFTER UPDATE OF end_zeit ON arbeits_logs
FOR EACH ROW
WHEN NEW.end_zeit IS NOT NULL
BEGIN
    UPDATE arbeits_logs 
    SET dauer_minuten = CAST((julianday(NEW.end_zeit) - julianday(NEW.start_zeit)) * 24 * 60 AS INTEGER)
    WHERE id = NEW.id;
END;
```

## Views für häufige Abfragen

### Aktive Aufgaben
```sql
CREATE VIEW v_active_tasks AS
SELECT 
    a.id,
    a.user_id,
    a.name AS aufgabe_name,
    a.beschreibung AS aufgabe_beschreibung,
    a.status AS aufgabe_status,
    a.deadline,
    a.benoetigtes_energie_level,
    a.ist_wichtig,
    a.ist_dringend,
    p.id AS projekt_id,
    p.name AS projekt_name,
    l.id AS lebensbereich_id,
    l.name AS lebensbereich_name,
    (SELECT COUNT(*) FROM teilschritte t 
     WHERE t.aufgabe_id = a.id AND t.status != 'abgeschlossen') AS offene_teilschritte,
    COALESCE(
        (SELECT SUM(al.dauer_minuten)
         FROM arbeits_logs al
         WHERE al.entity_type = 'aufgabe' AND al.entity_id = a.id),
        0
    ) AS minuten_gearbeitet
FROM aufgaben a
JOIN projekte p ON a.projekt_id = p.id
JOIN lebensbereiche l ON p.lebensbereich_id = l.id
WHERE a.is_active = 1 
  AND a.status NOT IN ('abgeschlossen', 'abgebrochen')
  AND p.is_active = 1
  AND l.is_active = 1;
```

## Migrations-Strategie

### ID-Generierung in der Anwendung
```python
import uuid

def generate_id():
    return str(uuid.uuid4())

# Beim Einfügen
new_project = {
    'id': generate_id(),
    'name': 'Mein Projekt',
    # ...
}
```

### JSON-Handling
```python
import json

# Speichern
preferences = {'theme': 'dark', 'notifications': True}
preferences_json = json.dumps(preferences)

# Lesen
preferences = json.loads(preferences_json)
```

## Empfehlungen

1. **Verwenden Sie SQLite3 für:**
   - Lokale Entwicklung
   - Prototyping
   - Single-User Tests

2. **Planen Sie Migration zu PostgreSQL für:**
   - Multi-User-Betrieb
   - Produktion
   - Wenn Sie erweiterte Features brauchen

3. **Nutzen Sie ein ORM:**
   - SQLAlchemy (Python)
   - Prisma (Node.js)
   - Dies erleichtert später die Migration

4. **Implementieren Sie fehlende Features in der Anwendung:**
   - UUID-Generierung
   - JSON-Verarbeitung
   - Komplexe Validierungen
   - Zirkularitätsprüfungen