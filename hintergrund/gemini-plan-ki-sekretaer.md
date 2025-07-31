# Mein Plan zur Umsetzung des KI-Sekretärs (CS50 MVP)

Dieser Plan ist darauf ausgelegt, dich in ca. 50 Stunden zu einem vorzeigbaren, funktionierenden Prototyp von Modul 1 zu führen.

---

## Phase 1: Das Backend-Fundament (ca. 20 Stunden)

**Ziel:** Eine funktionierende API, die Aufgaben speichern und abrufen kann, noch ganz ohne KI.

1.  **Projektstruktur anlegen:** Erstellen der grundlegenden Ordner und Dateien (`app.py`, `templates/`, `static/`).
2.  **Datenbank-Setup (Lokal mit SQLite):**
    *   Definition einer einfachen `tasks` Tabelle. Eine gute Basis ist: `id`, `user_id`, `title`, `description`, `status`, `created_at`, `due_date`.
    *   Erstellen der Datenbank mit SQLAlchemy in Flask.
3.  **API-Endpunkte in Flask erstellen:**
    *   `/api/tasks` (GET): Gibt alle erfassten Aufgaben als JSON zurück.
    *   `/api/tasks` (POST): Nimmt JSON-Daten entgegen und speichert eine neue Aufgabe in der Datenbank.
    *   `/api/secretary` (POST): Der zentrale Endpunkt, der die Nutzereingabe empfängt und später die KI-Logik anstößt.

---

## Phase 2: Das Frontend & die „Konversation“ (ca. 15 Stunden)

**Ziel:** Eine Benutzeroberfläche, auf der du mit dem Sekretär "chatten" kannst.

1.  **Einfaches HTML-Interface:**
    *   Ein Texteingabefeld für den Nutzer.
    *   Ein "Senden"-Button.
    *   Ein Bereich, in dem der "Chatverlauf" mit dem Sekretär angezeigt wird.
2.  **JavaScript-Logik (`fetch`):**
    *   Wenn der Nutzer auf "Senden" klickt, wird der Text aus dem Eingabefeld per `fetch` an deinen `/api/secretary` Endpunkt geschickt.
    *   Die Antwort vom Backend (z.B. "OK, habe ich notiert" oder eine Rückfrage) wird im Chatverlauf angezeigt.
    *   In dieser Phase antwortet der Sekretär nur mit fest programmierten Antworten, um den Ablauf zu testen.

---

## Phase 3: Die LLM-Integration (ca. 15 Stunden)

**Ziel:** Den Sekretär intelligent machen.

1.  **LLM-API-Anbindung:**
    *   Entscheidung für eine kommerzielle API (z.B. OpenAI) und Erstellung eines API-Keys.
    *   Im `/api/secretary` Endpunkt in Flask wird nun die LLM-API mit der Nutzereingabe aufgerufen.
2.  **Prompt Engineering (Das Herzstück):**
    *   Schreiben eines guten **System-Prompts**, der die "Stellenbeschreibung" für die KI ist.
    *   **Beispiel-System-Prompt:**
        > "Du bist ein ultra-effizienter Sekretär für eine Person mit ADHS. Deine Aufgabe ist es, unstrukturierte Eingaben in klar definierte Aufgaben umzuwandeln. Extrahiere immer folgende Informationen: `title`, `description`, `due_date`. Wenn eine Information fehlt, stelle eine einzige, klare Rückfrage. Antworte IMMER im folgenden JSON-Format: `{"status": "success", "task": {"title": "...", "description": "...", "due_date": "..."}}` oder `{"status": "incomplete", "question": "Deine Rückfrage hier."}`"
3.  **Antwort verarbeiten:**
    *   Die JSON-Antwort des LLM wird vom Flask-Backend empfangen.
    *   Wenn `status == "success"`, werden die Task-Daten in die Datenbank gespeichert.
    *   Wenn `status == "incomplete"`, wird die `question` an das Frontend geschickt und dem Nutzer angezeigt.

---

## Zusammenfassung des Vorgehens

1.  **Lokal starten, Cloud später:** Vereinfacht den Einstieg massiv.
2.  **Fokus auf Modul 1:** Kalender und komplexe Planungslogik bewusst ignorieren.
3.  **Backend zuerst:** Eine solide API und Datenbank sind die Basis.
4.  **Frontend als simple Schnittstelle:** Nur das Nötigste für die Interaktion.
5.  **KI als letzte Schicht:** Die Intelligenz wird an die bestehende Struktur "angeflanscht".
