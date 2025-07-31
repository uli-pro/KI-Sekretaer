# ADHS-App Datenbankschema

## Übersicht
Dieses Schema ist für eine Multi-User ADHS-App konzipiert, die bis zu 5000 Benutzer unterstützt. Die Struktur berücksichtigt die hierarchische Organisation von Lebensbereichen → Projekten → Aufgaben → Teilschritten mit flexiblen Abhängigkeiten und umfassender Zeiterfassung.

## Kern-Tabellen

### 1. users
Zentrale Benutzerverwaltung
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    timezone VARCHAR(50) DEFAULT 'Europe/Berlin',
    locale VARCHAR(10) DEFAULT 'de_DE',
    energy_pattern JSON, -- Tageszeitmuster für Energielevel
    adhd_preferences JSON, -- ADHS-spezifische Einstellungen
    notification_settings JSON,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT true,
    email_verified BOOLEAN DEFAULT false,
    CONSTRAINT chk_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_active ON users(is_active) WHERE is_active = true;
```

### 2. lebensbereiche
Oberste Organisationsebene
```sql
CREATE TABLE lebensbereiche (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    beschreibung TEXT,
    farbe VARCHAR(7) DEFAULT '#808080', -- HEX-Farbcode
    prioritaet INTEGER CHECK (prioritaet BETWEEN 1 AND 5),
    woechentlich_verfuegbare_zeit INTEGER, -- in Minuten
    bevorzugte_tageszeiten JSON, -- Array von Zeitfenstern
    user_eingaben_raw TEXT[], -- Unverarbeitete Texteingaben
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_farbe CHECK (farbe ~* '^#[0-9A-Fa-f]{6}$'),
    CONSTRAINT unq_user_lebensbereich UNIQUE(user_id, name)
);

CREATE INDEX idx_lebensbereiche_user ON lebensbereiche(user_id);
CREATE INDEX idx_lebensbereiche_active ON lebensbereiche(user_id, is_active) WHERE is_active = true;
```

### 3. projekte
Projekte innerhalb von Lebensbereichen
```sql
CREATE TABLE projekte (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    lebensbereich_id UUID NOT NULL REFERENCES lebensbereiche(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    beschreibung TEXT,
    farbe VARCHAR(7) DEFAULT '#808080',
    ist_wichtig BOOLEAN DEFAULT false,
    ist_dringend BOOLEAN DEFAULT false,
    status VARCHAR(50) NOT NULL DEFAULT 'offen',
    aufwand_geschaetzt_min INTEGER, -- in Minuten
    aufwand_geschaetzt_max INTEGER, -- in Minuten
    aufwand_tatsaechlich INTEGER, -- berechnet aus Logs
    deadline DATE,
    startdatum DATE,
    user_eingaben_raw TEXT[],
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT chk_status CHECK (status IN ('offen', 'begonnen', 'verschoben', 'abgeschlossen', 'abgebrochen')),
    CONSTRAINT chk_aufwand CHECK (aufwand_geschaetzt_min <= aufwand_geschaetzt_max),
    CONSTRAINT chk_farbe CHECK (farbe ~* '^#[0-9A-Fa-f]{6}$')
);

CREATE INDEX idx_projekte_user ON projekte(user_id);
CREATE INDEX idx_projekte_lebensbereich ON projekte(lebensbereich_id);
CREATE INDEX idx_projekte_status ON projekte(user_id, status);
CREATE INDEX idx_projekte_deadline ON projekte(deadline) WHERE deadline IS NOT NULL;
```

### 4. aufgaben
Aufgaben innerhalb von Projekten
```sql
CREATE TABLE aufgaben (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    projekt_id UUID NOT NULL REFERENCES projekte(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    beschreibung TEXT,
    farbe VARCHAR(7) DEFAULT '#808080',
    benoetigtes_energie_level INTEGER CHECK (benoetigtes_energie_level BETWEEN 1 AND 3),
    ist_wichtig BOOLEAN DEFAULT false,
    ist_dringend BOOLEAN DEFAULT false,
    status VARCHAR(50) NOT NULL DEFAULT 'offen',
    aufwand_geschaetzt_min INTEGER,
    aufwand_geschaetzt_max INTEGER,
    aufwand_tatsaechlich INTEGER,
    deadline TIMESTAMP WITH TIME ZONE,
    startdatum DATE,
    user_eingaben_raw TEXT[],
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT chk_status CHECK (status IN ('offen', 'begonnen', 'verschoben', 'abgeschlossen', 'abgebrochen')),
    CONSTRAINT chk_aufwand CHECK (aufwand_geschaetzt_min <= aufwand_geschaetzt_max),
    CONSTRAINT chk_farbe CHECK (farbe ~* '^#[0-9A-Fa-f]{6}$')
);

CREATE INDEX idx_aufgaben_user ON aufgaben(user_id);
CREATE INDEX idx_aufgaben_projekt ON aufgaben(projekt_id);
CREATE INDEX idx_aufgaben_status ON aufgaben(user_id, status);
CREATE INDEX idx_aufgaben_deadline ON aufgaben(deadline) WHERE deadline IS NOT NULL;
CREATE INDEX idx_aufgaben_energie ON aufgaben(benoetigtes_energie_level);
```

### 5. teilschritte
Konkrete Teilschritte einer Aufgabe
```sql
CREATE TABLE teilschritte (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    aufgabe_id UUID NOT NULL REFERENCES aufgaben(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    beschreibung TEXT,
    farbe VARCHAR(7) DEFAULT '#808080',
    reihenfolge_nummer INTEGER NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'offen',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    CONSTRAINT chk_status CHECK (status IN ('offen', 'begonnen', 'verschoben', 'abgeschlossen', 'abgebrochen')),
    CONSTRAINT chk_farbe CHECK (farbe ~* '^#[0-9A-Fa-f]{6}$'),
    CONSTRAINT unq_aufgabe_reihenfolge UNIQUE(aufgabe_id, reihenfolge_nummer)
);

CREATE INDEX idx_teilschritte_user ON teilschritte(user_id);
CREATE INDEX idx_teilschritte_aufgabe ON teilschritte(aufgabe_id);
CREATE INDEX idx_teilschritte_status ON teilschritte(user_id, status);
```

## Personen & Rollen

### 6. personen
Globale Personenverwaltung
```sql
CREATE TABLE personen (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    vorname VARCHAR(100),
    nachname VARCHAR(100),
    anzeigename VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    telefon VARCHAR(50),
    notizen TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_email CHECK (email IS NULL OR email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

CREATE INDEX idx_personen_user ON personen(user_id);
CREATE INDEX idx_personen_name ON personen(user_id, anzeigename);
```

### 7. rollen
Vordefinierte und benutzerdefinierte Rollen
```sql
CREATE TABLE rollen (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE, -- NULL für System-Rollen
    name VARCHAR(100) NOT NULL,
    beschreibung TEXT,
    is_system_rolle BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unq_rolle_name UNIQUE(user_id, name)
);

-- System-Rollen einfügen
INSERT INTO rollen (name, beschreibung, is_system_rolle) VALUES
    ('Auftraggeber', 'Person, die eine Aufgabe in Auftrag gibt', true),
    ('Ausführender', 'Person, die eine Aufgabe ausführt', true),
    ('Berater', 'Person, die beratend zur Seite steht', true),
    ('Prüfer', 'Person, die Ergebnisse prüft', true),
    ('Informant', 'Person, die Informationen bereitstellt', true);
```

### 8. personen_zuordnungen
Verknüpfung von Personen mit Entitäten und deren Rollen
```sql
CREATE TABLE personen_zuordnungen (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    person_id UUID NOT NULL REFERENCES personen(id) ON DELETE CASCADE,
    rolle_id UUID NOT NULL REFERENCES rollen(id) ON DELETE CASCADE,
    entity_type VARCHAR(50) NOT NULL,
    entity_id UUID NOT NULL,
    notizen TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_entity_type CHECK (entity_type IN ('lebensbereich', 'projekt', 'aufgabe', 'teilschritt'))
);

CREATE INDEX idx_personen_zuord_person ON personen_zuordnungen(person_id);
CREATE INDEX idx_personen_zuord_entity ON personen_zuordnungen(entity_type, entity_id);
```

## Tags & Kategorisierung

### 9. tags
Globale Tag-Verwaltung
```sql
CREATE TABLE tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE, -- NULL für System-Tags
    name VARCHAR(50) NOT NULL,
    farbe VARCHAR(7) DEFAULT '#808080',
    kategorie VARCHAR(50),
    is_system_tag BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_farbe CHECK (farbe ~* '^#[0-9A-Fa-f]{6}$'),
    CONSTRAINT unq_tag_name UNIQUE(user_id, name)
);

-- Beispiel-System-Tags
INSERT INTO tags (name, kategorie, farbe, is_system_tag) VALUES
    ('Schnell erledigt', 'Zeit', '#00FF00', true),
    ('Kreativ', 'Art', '#FF00FF', true),
    ('Routine', 'Art', '#0000FF', true),
    ('Kommunikation', 'Art', '#FFFF00', true),
    ('Konzentration', 'Energie', '#FF0000', true),
    ('Bewegung', 'Art', '#00FFFF', true);
```

### 10. tag_zuordnungen
Verknüpfung von Tags mit Entitäten
```sql
CREATE TABLE tag_zuordnungen (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tag_id UUID NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    entity_type VARCHAR(50) NOT NULL,
    entity_id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_entity_type CHECK (entity_type IN ('projekt', 'aufgabe')),
    CONSTRAINT unq_tag_entity UNIQUE(tag_id, entity_type, entity_id)
);

CREATE INDEX idx_tag_zuord_tag ON tag_zuordnungen(tag_id);
CREATE INDEX idx_tag_zuord_entity ON tag_zuordnungen(entity_type, entity_id);
```

## Abhängigkeiten

### 11. abhaengigkeiten
Flexible Abhängigkeiten zwischen allen Ebenen
```sql
CREATE TABLE abhaengigkeiten (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Abhängige Entität (wartet auf...)
    abhaengig_type VARCHAR(50) NOT NULL,
    abhaengig_id UUID NOT NULL,
    
    -- Voraussetzung (muss erledigt sein)
    voraussetzung_type VARCHAR(50) NOT NULL,
    voraussetzung_id UUID NOT NULL,
    
    beschreibung TEXT,
    is_blocking BOOLEAN DEFAULT true, -- Harte vs. weiche Abhängigkeit
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_abhaengig_type CHECK (abhaengig_type IN ('projekt', 'aufgabe', 'teilschritt')),
    CONSTRAINT chk_voraussetzung_type CHECK (voraussetzung_type IN ('projekt', 'aufgabe', 'teilschritt')),
    CONSTRAINT chk_no_self_dependency CHECK (NOT (abhaengig_type = voraussetzung_type AND abhaengig_id = voraussetzung_id)),
    CONSTRAINT unq_abhaengigkeit UNIQUE(abhaengig_type, abhaengig_id, voraussetzung_type, voraussetzung_id)
);

CREATE INDEX idx_abhaeng_user ON abhaengigkeiten(user_id);
CREATE INDEX idx_abhaeng_abhaengig ON abhaengigkeiten(abhaengig_type, abhaengig_id);
CREATE INDEX idx_abhaeng_voraussetzung ON abhaengigkeiten(voraussetzung_type, voraussetzung_id);
```

## Zeiterfassung & Logs

### 12. arbeits_logs
Detaillierte Zeiterfassung
```sql
CREATE TABLE arbeits_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    entity_type VARCHAR(50) NOT NULL,
    entity_id UUID NOT NULL,
    aktion VARCHAR(50) NOT NULL,
    start_zeit TIMESTAMP WITH TIME ZONE NOT NULL,
    end_zeit TIMESTAMP WITH TIME ZONE,
    dauer_minuten INTEGER GENERATED ALWAYS AS (
        CASE 
            WHEN end_zeit IS NOT NULL 
            THEN EXTRACT(EPOCH FROM (end_zeit - start_zeit)) / 60
            ELSE NULL 
        END
    ) STORED,
    energie_level INTEGER CHECK (energie_level BETWEEN 1 AND 3),
    notizen TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_entity_type CHECK (entity_type IN ('projekt', 'aufgabe', 'teilschritt')),
    CONSTRAINT chk_aktion CHECK (aktion IN ('angelegt', 'begonnen', 'bearbeitet', 'pausiert', 'fortgesetzt', 'abgeschlossen', 'abgebrochen')),
    CONSTRAINT chk_zeit CHECK (end_zeit IS NULL OR end_zeit > start_zeit)
);

CREATE INDEX idx_logs_user ON arbeits_logs(user_id);
CREATE INDEX idx_logs_entity ON arbeits_logs(entity_type, entity_id);
CREATE INDEX idx_logs_zeit ON arbeits_logs(user_id, start_zeit);
CREATE INDEX idx_logs_active ON arbeits_logs(user_id, end_zeit) WHERE end_zeit IS NULL;
```

### 13. status_history
Historie von Statusänderungen
```sql
CREATE TABLE status_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type VARCHAR(50) NOT NULL,
    entity_id UUID NOT NULL,
    old_status VARCHAR(50),
    new_status VARCHAR(50) NOT NULL,
    changed_by UUID NOT NULL REFERENCES users(id),
    changed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    reason TEXT,
    CONSTRAINT chk_entity_type CHECK (entity_type IN ('projekt', 'aufgabe', 'teilschritt'))
);

CREATE INDEX idx_status_hist_entity ON status_history(entity_type, entity_id);
CREATE INDEX idx_status_hist_time ON status_history(changed_at);
```

## Wiederholende Aufgaben

### 14. wiederholungsmuster
Definition von Wiederholungsmustern
```sql
CREATE TABLE wiederholungsmuster (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255),
    muster_typ VARCHAR(50) NOT NULL,
    konfiguration JSON NOT NULL,
    start_datum DATE NOT NULL,
    end_datum DATE,
    naechste_ausfuehrung TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_muster_typ CHECK (muster_typ IN ('stündlich', 'täglich', 'wochentage', 'wöchentlich', 'monatstage', 'monatlich', 'jährlich'))
);

CREATE INDEX idx_wiederholung_user ON wiederholungsmuster(user_id);
CREATE INDEX idx_wiederholung_next ON wiederholungsmuster(naechste_ausfuehrung) WHERE is_active = true;
```

### 15. wiederholende_entitaeten
Verknüpfung von Projekten/Aufgaben mit Wiederholungsmustern
```sql
CREATE TABLE wiederholende_entitaeten (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    wiederholungsmuster_id UUID NOT NULL REFERENCES wiederholungsmuster(id) ON DELETE CASCADE,
    template_type VARCHAR(50) NOT NULL,
    template_id UUID NOT NULL, -- ID des Original-Projekts/der Original-Aufgabe
    letzte_erstellung TIMESTAMP WITH TIME ZONE,
    anzahl_erstellt INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_template_type CHECK (template_type IN ('projekt', 'aufgabe'))
);

CREATE INDEX idx_wiederhol_muster ON wiederholende_entitaeten(wiederholungsmuster_id);
CREATE INDEX idx_wiederhol_template ON wiederholende_entitaeten(template_type, template_id);
```

## Hilfs-Tabellen

### 16. benachrichtigungen
Benachrichtigungssystem
```sql
CREATE TABLE benachrichtigungen (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    typ VARCHAR(50) NOT NULL,
    titel VARCHAR(255) NOT NULL,
    nachricht TEXT,
    entity_type VARCHAR(50),
    entity_id UUID,
    geplant_fuer TIMESTAMP WITH TIME ZONE NOT NULL,
    gesendet_am TIMESTAMP WITH TIME ZONE,
    gelesen_am TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_typ CHECK (typ IN ('erinnerung', 'deadline', 'status_update', 'abhängigkeit', 'energie'))
);

CREATE INDEX idx_benachricht_user ON benachrichtigungen(user_id);
CREATE INDEX idx_benachricht_pending ON benachrichtigungen(user_id, geplant_fuer) WHERE gesendet_am IS NULL;
CREATE INDEX idx_benachricht_unread ON benachrichtigungen(user_id, gelesen_am) WHERE gelesen_am IS NULL;
```

### 17. user_sessions
Session-Management
```sql
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) UNIQUE NOT NULL,
    device_info JSON,
    ip_address INET,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    last_activity TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

CREATE INDEX idx_sessions_user ON user_sessions(user_id);
CREATE INDEX idx_sessions_token ON user_sessions(token_hash);
CREATE INDEX idx_sessions_active ON user_sessions(user_id, is_active) WHERE is_active = true;
```

## Views für häufige Abfragen

### Aktive Aufgaben mit vollständigem Kontext
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
    COALESCE(
        (SELECT JSON_AGG(t.name ORDER BY t.reihenfolge_nummer)
         FROM teilschritte t
         WHERE t.aufgabe_id = a.id AND t.status != 'abgeschlossen'),
        '[]'::JSON
    ) AS offene_teilschritte,
    COALESCE(
        (SELECT SUM(al.dauer_minuten)
         FROM arbeits_logs al
         WHERE al.entity_type = 'aufgabe' AND al.entity_id = a.id),
        0
    ) AS minuten_gearbeitet
FROM aufgaben a
JOIN projekte p ON a.projekt_id = p.id
JOIN lebensbereiche l ON p.lebensbereich_id = l.id
WHERE a.is_active = true 
  AND a.status NOT IN ('abgeschlossen', 'abgebrochen')
  AND p.is_active = true
  AND l.is_active = true;
```

### Abhängigkeitsbaum
```sql
CREATE VIEW v_dependency_tree AS
WITH RECURSIVE dep_tree AS (
    -- Basis: Direkte Abhängigkeiten
    SELECT 
        d.id,
        d.user_id,
        d.abhaengig_type,
        d.abhaengig_id,
        d.voraussetzung_type,
        d.voraussetzung_id,
        d.is_blocking,
        1 as level,
        ARRAY[ROW(d.abhaengig_type, d.abhaengig_id)::TEXT] as path
    FROM abhaengigkeiten d
    
    UNION ALL
    
    -- Rekursion: Transitive Abhängigkeiten
    SELECT 
        d.id,
        d.user_id,
        d.abhaengig_type,
        d.abhaengig_id,
        dt.voraussetzung_type,
        dt.voraussetzung_id,
        d.is_blocking AND dt.is_blocking,
        dt.level + 1,
        dt.path || ROW(d.abhaengig_type, d.abhaengig_id)::TEXT
    FROM abhaengigkeiten d
    JOIN dep_tree dt ON d.voraussetzung_type = dt.abhaengig_type 
                    AND d.voraussetzung_id = dt.abhaengig_id
    WHERE NOT ROW(d.abhaengig_type, d.abhaengig_id)::TEXT = ANY(dt.path) -- Zyklus-Prävention
)
SELECT * FROM dep_tree;
```

## Stored Procedures & Functions

### Zirkuläre Abhängigkeiten prüfen
```sql
CREATE OR REPLACE FUNCTION check_circular_dependency(
    p_abhaengig_type VARCHAR,
    p_abhaengig_id UUID,
    p_voraussetzung_type VARCHAR,
    p_voraussetzung_id UUID,
    p_user_id UUID
) RETURNS BOOLEAN AS $$
DECLARE
    v_has_circular BOOLEAN;
BEGIN
    WITH RECURSIVE dep_check AS (
        SELECT 
            voraussetzung_type,
            voraussetzung_id,
            ARRAY[ROW(p_abhaengig_type, p_abhaengig_id)::TEXT] as path
        FROM abhaengigkeiten
        WHERE abhaengig_type = p_voraussetzung_type 
          AND abhaengig_id = p_voraussetzung_id
          AND user_id = p_user_id
        
        UNION ALL
        
        SELECT 
            d.voraussetzung_type,
            d.voraussetzung_id,
            dc.path || ROW(d.abhaengig_type, d.abhaengig_id)::TEXT
        FROM abhaengigkeiten d
        JOIN dep_check dc ON d.abhaengig_type = dc.voraussetzung_type 
                         AND d.abhaengig_id = dc.voraussetzung_id
        WHERE d.user_id = p_user_id
          AND NOT ROW(d.abhaengig_type, d.abhaengig_id)::TEXT = ANY(dc.path)
    )
    SELECT EXISTS (
        SELECT 1 FROM dep_check 
        WHERE voraussetzung_type = p_abhaengig_type 
          AND voraussetzung_id = p_abhaengig_id
    ) INTO v_has_circular;
    
    RETURN v_has_circular;
END;
$$ LANGUAGE plpgsql;
```

### Trigger für automatische Zeitstempel
```sql
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger für alle relevanten Tabellen
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
    
CREATE TRIGGER update_lebensbereiche_updated_at BEFORE UPDATE ON lebensbereiche
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
    
-- ... (weitere Trigger für andere Tabellen)
```

### Aufwand berechnen
```sql
CREATE OR REPLACE FUNCTION calculate_actual_effort()
RETURNS TRIGGER AS $$
DECLARE
    v_total_minutes INTEGER;
BEGIN
    -- Berechne Gesamtaufwand aus Logs
    SELECT COALESCE(SUM(dauer_minuten), 0)
    INTO v_total_minutes
    FROM arbeits_logs
    WHERE entity_type = TG_ARGV[0]
      AND entity_id = NEW.id;
    
    -- Update aufwand_tatsaechlich
    NEW.aufwand_tatsaechlich = v_total_minutes;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger für Projekte und Aufgaben
CREATE TRIGGER calc_projekt_effort BEFORE UPDATE ON projekte
    FOR EACH ROW 
    WHEN (NEW.status = 'abgeschlossen')
    EXECUTE FUNCTION calculate_actual_effort('projekt');
    
CREATE TRIGGER calc_aufgabe_effort BEFORE UPDATE ON aufgaben
    FOR EACH ROW 
    WHEN (NEW.status = 'abgeschlossen')
    EXECUTE FUNCTION calculate_actual_effort('aufgabe');
```

## Indizes für Performance

```sql
-- Zusammengesetzte Indizes für häufige Queries
CREATE INDEX idx_projekte_user_status ON projekte(user_id, status) WHERE is_active = true;
CREATE INDEX idx_aufgaben_user_deadline ON aufgaben(user_id, deadline) WHERE status NOT IN ('abgeschlossen', 'abgebrochen');
CREATE INDEX idx_aufgaben_energie_status ON aufgaben(user_id, benoetigtes_energie_level, status) WHERE is_active = true;

-- Partial Indizes für aktive Einträge
CREATE INDEX idx_active_projects ON projekte(user_id) WHERE is_active = true AND status NOT IN ('abgeschlossen', 'abgebrochen');
CREATE INDEX idx_active_tasks ON aufgaben(user_id) WHERE is_active = true AND status NOT IN ('abgeschlossen', 'abgebrochen');

-- Index für Volltextsuche
CREATE INDEX idx_projekte_search ON projekte USING gin(to_tsvector('german', name || ' ' || COALESCE(beschreibung, '')));
CREATE INDEX idx_aufgaben_search ON aufgaben USING gin(to_tsvector('german', name || ' ' || COALESCE(beschreibung, '')));
```

## Sicherheit & Datenschutz

### Row Level Security (RLS)
```sql
-- RLS aktivieren
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE lebensbereiche ENABLE ROW LEVEL SECURITY;
ALTER TABLE projekte ENABLE ROW LEVEL SECURITY;
ALTER TABLE aufgaben ENABLE ROW LEVEL SECURITY;
ALTER TABLE teilschritte ENABLE ROW LEVEL SECURITY;

-- Policy für Benutzer: Nur eigene Daten sehen
CREATE POLICY users_own_data ON lebensbereiche
    FOR ALL
    USING (user_id = current_setting('app.current_user_id')::UUID);

CREATE POLICY users_own_data ON projekte
    FOR ALL
    USING (user_id = current_setting('app.current_user_id')::UUID);

CREATE POLICY users_own_data ON aufgaben
    FOR ALL
    USING (user_id = current_setting('app.current_user_id')::UUID);

CREATE POLICY users_own_data ON teilschritte
    FOR ALL
    USING (user_id = current_setting('app.current_user_id')::UUID);

-- Weitere Policies für andere Tabellen...
```

## Optimierungen für ADHS-spezifische Features

### Energie-Tracking View
```sql
CREATE VIEW v_energie_analyse AS
SELECT 
    u.id AS user_id,
    DATE(al.start_zeit) AS datum,
    EXTRACT(HOUR FROM al.start_zeit) AS stunde,
    al.energie_level,
    COUNT(*) AS anzahl_aktivitaeten,
    SUM(al.dauer_minuten) AS gesamt_minuten,
    AVG(al.dauer_minuten) AS durchschnitt_minuten
FROM users u
JOIN arbeits_logs al ON u.id = al.user_id
WHERE al.energie_level IS NOT NULL
GROUP BY u.id, DATE(al.start_zeit), EXTRACT(HOUR FROM al.start_zeit), al.energie_level;
```

### Prokrastinations-Erkennung
```sql
CREATE VIEW v_prokrastination_kandidaten AS
SELECT 
    a.*,
    CURRENT_DATE - a.startdatum::DATE AS tage_seit_start,
    a.deadline::DATE - CURRENT_DATE AS tage_bis_deadline,
    COALESCE(
        (SELECT MAX(al.start_zeit)
         FROM arbeits_logs al
         WHERE al.entity_type = 'aufgabe' AND al.entity_id = a.id),
        a.created_at
    ) AS letzte_aktivitaet,
    CURRENT_TIMESTAMP - COALESCE(
        (SELECT MAX(al.start_zeit)
         FROM arbeits_logs al
         WHERE al.entity_type = 'aufgabe' AND al.entity_id = a.id),
        a.created_at
    ) AS zeit_seit_letzter_aktivitaet
FROM aufgaben a
WHERE a.status IN ('offen', 'begonnen')
  AND a.is_active = true
  AND (
    -- Lange nicht bearbeitet
    CURRENT_TIMESTAMP - COALESCE(
        (SELECT MAX(al.start_zeit)
         FROM arbeits_logs al
         WHERE al.entity_type = 'aufgabe' AND al.entity_id = a.id),
        a.created_at
    ) > INTERVAL '7 days'
    OR
    -- Deadline naht und wenig Fortschritt
    (a.deadline IS NOT NULL 
     AND a.deadline::DATE - CURRENT_DATE < 7
     AND COALESCE(a.aufwand_tatsaechlich, 0) < COALESCE(a.aufwand_geschaetzt_min, 60) * 0.3)
  );
```

## Datenintegrität & Constraints

### Check Constraints für Geschäftlogik
```sql
-- Projekte können nur abgeschlossen werden, wenn alle Aufgaben erledigt sind
CREATE OR REPLACE FUNCTION check_projekt_completion()
RETURNS TRIGGER AS $
BEGIN
    IF NEW.status = 'abgeschlossen' AND OLD.status != 'abgeschlossen' THEN
        IF EXISTS (
            SELECT 1 FROM aufgaben 
            WHERE projekt_id = NEW.id 
              AND status NOT IN ('abgeschlossen', 'abgebrochen')
              AND is_active = true
        ) THEN
            RAISE EXCEPTION 'Projekt kann nicht abgeschlossen werden: Es gibt noch offene Aufgaben';
        END IF;
    END IF;
    RETURN NEW;
END;
$ LANGUAGE plpgsql;

CREATE TRIGGER check_projekt_completion_trigger
    BEFORE UPDATE ON projekte
    FOR EACH ROW
    EXECUTE FUNCTION check_projekt_completion();

-- Ähnliche Trigger für Aufgaben und Teilschritte...
```

### Automatische Wiederholung erstellen
```sql
CREATE OR REPLACE FUNCTION create_recurring_instances()
RETURNS INTEGER AS $
DECLARE
    v_count INTEGER := 0;
    v_muster RECORD;
    v_template RECORD;
    v_new_id UUID;
BEGIN
    -- Durchlaufe alle aktiven Wiederholungsmuster
    FOR v_muster IN 
        SELECT * FROM wiederholungsmuster 
        WHERE is_active = true 
          AND naechste_ausfuehrung <= CURRENT_TIMESTAMP
    LOOP
        -- Hole Template-Informationen
        FOR v_template IN 
            SELECT * FROM wiederholende_entitaeten 
            WHERE wiederholungsmuster_id = v_muster.id
        LOOP
            -- Erstelle neue Instanz basierend auf Template
            IF v_template.template_type = 'projekt' THEN
                -- Projekt kopieren
                INSERT INTO projekte (
                    user_id, lebensbereich_id, name, beschreibung, 
                    farbe, ist_wichtig, ist_dringend, status,
                    aufwand_geschaetzt_min, aufwand_geschaetzt_max
                )
                SELECT 
                    user_id, lebensbereich_id, 
                    name || ' (' || TO_CHAR(CURRENT_DATE, 'DD.MM.YYYY') || ')',
                    beschreibung, farbe, ist_wichtig, ist_dringend, 'offen',
                    aufwand_geschaetzt_min, aufwand_geschaetzt_max
                FROM projekte
                WHERE id = v_template.template_id
                RETURNING id INTO v_new_id;
                
                -- Aufgaben des Projekts kopieren
                INSERT INTO aufgaben (
                    user_id, projekt_id, name, beschreibung, farbe,
                    benoetigtes_energie_level, ist_wichtig, ist_dringend, status
                )
                SELECT 
                    user_id, v_new_id, name, beschreibung, farbe,
                    benoetigtes_energie_level, ist_wichtig, ist_dringend, 'offen'
                FROM aufgaben
                WHERE projekt_id = v_template.template_id;
                
            ELSIF v_template.template_type = 'aufgabe' THEN
                -- Aufgabe kopieren
                INSERT INTO aufgaben (
                    user_id, projekt_id, name, beschreibung, farbe,
                    benoetigtes_energie_level, ist_wichtig, ist_dringend, status,
                    aufwand_geschaetzt_min, aufwand_geschaetzt_max
                )
                SELECT 
                    user_id, projekt_id,
                    name || ' (' || TO_CHAR(CURRENT_DATE, 'DD.MM.YYYY') || ')',
                    beschreibung, farbe, benoetigtes_energie_level, 
                    ist_wichtig, ist_dringend, 'offen',
                    aufwand_geschaetzt_min, aufwand_geschaetzt_max
                FROM aufgaben
                WHERE id = v_template.template_id
                RETURNING id INTO v_new_id;
                
                -- Teilschritte kopieren
                INSERT INTO teilschritte (
                    user_id, aufgabe_id, name, beschreibung, farbe,
                    reihenfolge_nummer, status
                )
                SELECT 
                    user_id, v_new_id, name, beschreibung, farbe,
                    reihenfolge_nummer, 'offen'
                FROM teilschritte
                WHERE aufgabe_id = v_template.template_id;
            END IF;
            
            -- Update letzte Erstellung
            UPDATE wiederholende_entitaeten
            SET letzte_erstellung = CURRENT_TIMESTAMP,
                anzahl_erstellt = anzahl_erstellt + 1
            WHERE id = v_template.id;
            
            v_count := v_count + 1;
        END LOOP;
        
        -- Berechne nächste Ausführung basierend auf Muster
        UPDATE wiederholungsmuster
        SET naechste_ausfuehrung = calculate_next_occurrence(id)
        WHERE id = v_muster.id;
    END LOOP;
    
    RETURN v_count;
END;
$ LANGUAGE plpgsql;

-- Funktion zur Berechnung der nächsten Ausführung
CREATE OR REPLACE FUNCTION calculate_next_occurrence(p_muster_id UUID)
RETURNS TIMESTAMP WITH TIME ZONE AS $
DECLARE
    v_muster RECORD;
    v_next TIMESTAMP WITH TIME ZONE;
BEGIN
    SELECT * INTO v_muster FROM wiederholungsmuster WHERE id = p_muster_id;
    
    CASE v_muster.muster_typ
        WHEN 'täglich' THEN
            v_next := CURRENT_TIMESTAMP + (v_muster.konfiguration->>'interval')::INTERVAL;
        WHEN 'wöchentlich' THEN
            v_next := CURRENT_TIMESTAMP + INTERVAL '1 week' * (v_muster.konfiguration->>'weeks')::INTEGER;
        WHEN 'monatlich' THEN
            v_next := CURRENT_TIMESTAMP + INTERVAL '1 month' * (v_muster.konfiguration->>'months')::INTEGER;
        -- Weitere Muster...
    END CASE;
    
    RETURN v_next;
END;
$ LANGUAGE plpgsql;
```

## Performance-Monitoring

### Statistik-Tabellen
```sql
CREATE TABLE performance_stats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    datum DATE NOT NULL,
    anzahl_erledigte_aufgaben INTEGER DEFAULT 0,
    anzahl_erledigte_teilschritte INTEGER DEFAULT 0,
    gesamt_minuten_gearbeitet INTEGER DEFAULT 0,
    durchschnitt_energie_level NUMERIC(3,2),
    produktivste_stunde INTEGER,
    anzahl_unterbrechungen INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unq_user_datum UNIQUE(user_id, datum)
);

CREATE INDEX idx_perf_stats_user_date ON performance_stats(user_id, datum DESC);
```

## Backup & Archivierung

### Archiv-Tabellen für abgeschlossene Elemente
```sql
CREATE TABLE archiv_projekte (
    LIKE projekte INCLUDING ALL,
    archived_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    archived_by UUID REFERENCES users(id)
);

CREATE TABLE archiv_aufgaben (
    LIKE aufgaben INCLUDING ALL,
    archived_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    archived_by UUID REFERENCES users(id)
);

-- Trigger für automatische Archivierung nach X Tagen
CREATE OR REPLACE FUNCTION auto_archive_completed()
RETURNS void AS $
BEGIN
    -- Archiviere Projekte die länger als 90 Tage abgeschlossen sind
    INSERT INTO archiv_projekte
    SELECT *, CURRENT_TIMESTAMP, user_id
    FROM projekte
    WHERE status = 'abgeschlossen'
      AND completed_at < CURRENT_TIMESTAMP - INTERVAL '90 days';
    
    -- Lösche archivierte Projekte
    DELETE FROM projekte
    WHERE status = 'abgeschlossen'
      AND completed_at < CURRENT_TIMESTAMP - INTERVAL '90 days';
    
    -- Ähnlich für Aufgaben...
END;
$ LANGUAGE plpgsql;
```

## Beispiel-Konfiguration für Wiederholungsmuster

```json
-- Täglich um 9:00 Uhr
{
    "type": "daily",
    "time": "09:00",
    "interval": 1
}

-- Jeden Montag, Mittwoch und Freitag um 14:00
{
    "type": "weekdays",
    "days": [1, 3, 5],
    "time": "14:00"
}

-- Jeden 15. des Monats
{
    "type": "monthly",
    "day": 15,
    "time": "10:00"
}

-- Jährlich am 1. Januar
{
    "type": "yearly",
    "month": 1,
    "day": 1,
    "time": "00:00"
}
```

## Empfehlungen für die Implementierung

1. **Partitionierung**: Bei 5000 Usern sollten Sie Tabellen wie `arbeits_logs` nach Datum partitionieren
2. **Caching**: Implementieren Sie Redis für häufig abgerufene Daten
3. **Queue-System**: Nutzen Sie ein Queue-System für Benachrichtigungen und wiederkehrende Aufgaben
4. **Monitoring**: Implementieren Sie Logging und Monitoring für Performance-Tracking
5. **Backup-Strategie**: Tägliche Backups mit Point-in-Time Recovery
6. **API-Rate-Limiting**: Implementieren Sie Rate-Limiting pro User
7. **Soft-Deletes**: Verwenden Sie `is_active` Flags statt harte Löschungen