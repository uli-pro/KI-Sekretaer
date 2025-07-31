# Umsetzungsplan: KI-Sekretär (CS50-MVP)

Dieser Plan ist das Ergebnis unserer gemeinsamen Analyse und kombiniert die pragmatische Vorgehensweise von Gemini mit der tiefen, empathischen Produktvision von Claude. Er ist darauf ausgelegt, Sie in ca. 50-60 Stunden zu einem beeindruckenden CS50-Final-Project zu führen.

## 1. Vision & Differenzierung

- **Problem:** Erwachsene mit ADHS kämpfen nicht nur mit Aufgabenmanagement, sondern auch mit der damit verbundenen emotionalen Last (Schuld, Überforderung).
- **Lösung:** Ein "nachsichtiger KI-Sekretär", der den "Schuld-und-Abbruch-Zyklus" durchbricht.
- **MVP-Fokus:** Eine einzige Funktion perfektionieren: **Das mühelose Erfassen und intelligente Zerlegen von Aufgaben mit einem Fokus auf die emotionale User Experience.**

## 2. Tech-Stack (Pragmatisch & CS50-konform)

- **Backend:** Python mit **Flask**
- **Datenbank:** **SQLite** (simpel, keine Server-Konfiguration nötig)
- **Frontend:** **HTML, CSS, Vanilla JavaScript** (keine komplexen Frameworks, um den Fokus auf der Kernlogik zu halten)
- **KI:** **OpenAI API** (einfach zu integrieren, kostenlose Start-Credits)
- **Deployment:** Lokal für die Entwicklung und die CS50-Abgabe.

## 3. Detaillierter 6-Wochen-Plan

### **Woche 1-2: Das Backend-Fundament (ca. 15-20 Stunden)**

**Ziel:** Eine funktionierende API, die Aufgaben speichern, lesen und löschen kann.

- **[ ] Projekt-Setup:** Flask-App-Struktur anlegen (`app.py`, `templates`, `static`).
- **[ ] Datenbank-Design:** Erstellen Sie das `task`-Modell in `models.py`.
  ```python
  # models.py
  from flask_sqlalchemy import SQLAlchemy
  db = SQLAlchemy()
  
  class Task(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      user_id = db.Column(db.Integer, nullable=False) # Für später
      raw_input = db.Column(db.String(500), nullable=False)
      title = db.Column(db.String(200), nullable=False)
      description = db.Column(db.Text, nullable=True)
      status = db.Column(db.String(50), default='pending')
      energy_required = db.Column(db.Integer, default=2) # 1=niedrig, 2=mittel, 3=hoch
      estimated_duration = db.Column(db.Integer, nullable=True) # in Minuten
      # Fügen Sie weitere Felder nach Bedarf hinzu
  ```
- **[ ] API-Endpunkte:** Erstellen Sie die grundlegenden Routen in `app.py`.
  - `POST /api/secretary`: Nimmt die unstrukturierte Eingabe des Nutzers entgegen. **Fürs Erste:** Speichern Sie die Eingabe einfach als `raw_input` und `title` in der DB.
  - `GET /api/tasks`: Gibt alle Aufgaben als JSON zurück.
  - `DELETE /api/tasks/<int:task_id>`: Löscht eine Aufgabe.
- **[ ] Testing:** Testen Sie Ihre Endpunkte mit einem Tool wie `curl` oder Postman.

### **Woche 3-4: Die KI-Integration & das "Gehirn" (ca. 15-20 Stunden)**

**Ziel:** Den Sekretär intelligent machen.

- **[ ] OpenAI-API-Key:** Besorgen und sicher als Umgebungsvariable speichern.
- **[ ] Prompt Engineering:** Dies ist der wichtigste Teil. Erstellen Sie eine Funktion `process_with_llm(raw_text)`.
  
  - **System-Prompt:** Definieren Sie die Rolle der KI.
    > "Du bist ein empathischer und unterstützender Sekretär für eine Person mit ADHS. Deine Aufgabe ist es, unstrukturierte Eingaben in eine klar definierte Aufgabe umzuwandeln. Extrahiere immer: `title`, `description`, `energy_required` (1-3), und `estimated_duration` (in Minuten). Wenn eine Information fehlt, stelle EINE EINZIGE, freundliche und klare Rückfrage. Antworte IMMER im folgenden JSON-Format: `{\"status\": \"success\", \"task\": {...}}` oder `{\"status\": \"incomplete\", \"question\": \"Deine Rückfrage.\"}`"
- **[ ] API-Call implementieren:** Rufen Sie in `POST /api/secretary` Ihre `process_with_llm`-Funktion auf.
- **[ ] Antwort verarbeiten:**
  - Wenn `status == "success"`, speichern Sie die extrahierten Daten in der Datenbank.
  - Wenn `status == "incomplete"`, senden Sie die `question` zurück an das Frontend.

### **Woche 5-6: Das Frontend & die "nachsichtige" UX (ca. 10-15 Stunden)**

**Ziel:** Ein Interface, das sich gut anfühlt und die CS50-Anforderungen erfüllt.

- **[ ] HTML-Struktur:** Erstellen Sie ein einfaches Interface in `templates/index.html`.
  - Ein großes, einladendes Texteingabefeld.
  - Ein "Senden"-Button.
  - Ein Bereich für den "Chat"-Verlauf.
  - Eine einfache Liste zur Anzeige der erstellten Aufgaben.
- **[ ] JavaScript-Logik (`static/js/main.js`):**
  - **`fetch` an `/api/secretary`:** Senden Sie die Nutzereingabe an Ihr Backend.
  - **Antwort-Handling:** Zeigen Sie die Antwort der KI (Bestätigung oder Rückfrage) im Chat-Bereich an.
  - **Aufgabenliste aktualisieren:** Rufen Sie `GET /api/tasks` auf, um die Aufgabenliste dynamisch zu aktualisieren, nachdem eine neue Aufgabe erstellt wurde.
- **[ ] "Nachsichtiges" Design:**
  - Verwenden Sie beruhigende Farben (z.B. Blau- und Grüntöne).
  - Vermeiden Sie aggressive Rottöne für Fehler.
  - Formulieren Sie alle Texte (Buttons, Platzhalter) positiv und ermutigend.
- **[ ] CS50-Anforderungen:**
  - Erstellen Sie eine umfassende `README.md`, die Ihr Projekt, die Design-Entscheidungen und die Dateistruktur erklärt.
  - Nehmen Sie ein 3-minütiges Video auf, das die Funktionalität demonstriert.

## 4. Erfolgskriterien für das CS50-MVP

- **[ ] Funktionalität:** Ein Nutzer kann einen Gedanken eingeben, die KI verarbeitet ihn, und eine strukturierte Aufgabe erscheint in der Liste.
- **[ ] KI-Interaktion:** Die KI stellt Rückfragen, wenn Informationen fehlen.
- **[ ] Datenbank:** Die Aufgaben werden persistent in SQLite gespeichert.
- **[ ] Frontend:** Das Interface ist sauber, reaktiv und demonstriert die Kernfunktionalität.
- **[ ] Dokumentation:** Die `README.md` und das Video sind vollständig und professionell.

Dieser Plan gibt Ihnen eine klare Struktur und Meilensteine. Viel Erfolg bei der Umsetzung
