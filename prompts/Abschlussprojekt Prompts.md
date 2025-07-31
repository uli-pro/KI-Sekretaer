# Prompts zur Vorbereitung und Durchführung des Abschlussprojekts

## Weiterarbeit an der ADHS App

ROLLE: Du bist ein erfahrener Software-Entwickler und Leiter von Entwicklungsteams. 

KONTEXT ZUM PROJEKT: 

Ich plane eine App für ADHS-Patienten. Ich denke an eine Art "elektronische Prothese" für ihre gestörten Exekutiv-Funktionen mit drei drei Modulen:

MODUL 1: Ein KI-basierter Sekretär für die text- und sprachgesteuerte Eingabe von Todos, Projekten, Aufgaben, Terminen und Verpflichtungen.  

Der Sekretär erfragt zu jeder Eingabe die nötigen Hintergrundinformationen und legt sie in einem Database ab. 

Beispiel:

Eingabe:  "Ich muss morgen eine E-Mail an Herrn Müller schreiben". Sekretär: "Worum geht es in der E-Mail?" Eingabe: "Um den Projektbericht zu XY." Sekretär: "Wie viel Vorbereitungszeit braucht die E-Mail? Hast du alle Fakten vorliegen, oder musst du sie erst beschaffen?" Eingabe: "Ich muss den Projektbericht noch fertig schreiben. Das dauert sicherlich zwei Stunden." Sekretär: "OK. Ich erstelle zwei Aufgaben: 1) Projektbericht fertig schreiben - 2 Stunden. 2) Projektbericht an Herrn Müller mailen - 15 Minunten. Ist das so in Ordnung oder fehlt noch etwas?" Eingabe: "Das ist in Ordnung."

MODUL 2: Ein KI-basierter Planungsassistent, der aufgrund des Daten im Database einen strukturierten Zeitplan erstellt: 

Beispiel:

Montag von 09:00-11:00 Uhr: Projektbericht für Herrn Müller schreiben. 
Von 11:00 bis 11:30 E-Mail an Herrn Müller; E-Mail-Postfach abarbeiten. 
Von 11:30 bis 12:30 Meeting mit Herrn Maier und Frau Schulze
Von 12:30 bis 13:00 Uhr: Protokoll des Meetings schreiben.

Der Planungsassistent erstellt Wochen- und Tagesplan selbstständig, fragt aber den User nach Feedback und arbeitet Korrekturen ein.

Noch wichtiger für ADHS-Patienten ist eine ständige "vergebende Anpassung": Wenn eine Aufgabe nicht erledigt werden oder Zeitplan nicht ganz eingehalten werden konnte, dann passt der Planungsassistent den Plan mit freundlichen und ermutigenden Worten an die neuen Gegebenheiten an. Dabei ist wichtig, dass er die Wichtigkeit und die Dringlichkeit der einzelnen Aufgaben und Termine richtig einschätzt. 

MODUL 3: Ein KI-gestütztes Fokuscoach zur Abarbeitung von Aufgaben. Der Fokuscoach bleibt oben rechts am Bildschirm in einem kleinen, semitransparenten Fenster eingeblendet. Er zeigt an, welche Aufgabe gerade bearbeitet werden muss und wieviel Zeit  noch zur Verfügung steht (vielleicht mit einer Pomodoro-Timer-artigen Grafik). 

Er kann aber noch mehr: Er zerlegt KI-gestützt die Aufgaben in kleinere Einzelschritte und zeigt diese ebenfalls an.

Beispiel: 

Schreibe Projektbericht für Herrn Müller: 09:00 bis 11:00 Uhr.

Jetzt: Überprüfe die gesammelten Daten (15 Minuten bis 09:15 Uhr)

Nächste Aufgabe: Schreibe die Einleitung für den Bericht (15 Minuten)

Auch der Fokuscoach passt sich stets an die real geleistete Arbeit an (dazu nutzt er im Hintergrund den Planungsassistenten).



KONTEXT ZU MEINER PERSON: Im Moment absolviere ich den Harvard-Computerkurs CS50, um mich mit den Grundlagen des Programmierens vertraut zu machen. Ich würde gerne als Abschlussprojekt eines der drei Module programmieren. Ich habe pro Woche ca 15 h Zeit für den CS50. Insgesamt habe ich ca. 50-60 h für das gesamte Abschlussprojekt eingeplant.



AUFGABE: Bitte evaluiere folgende Fragestellungen: 

1) Ist diese "Elektronische Prothese" realisierbar mit Hilfe von KI-Tools, die für einen Solo-Entwickler ohne Machine-Learning-Hintergrund zugänglich sind. Damit meine ich kommerzielle LLM's wie Claude 4 , Chat-GPT oder Google Gemini und / oder selbst gehosteten Open Source LLM's von Hugging Face oder GitHub. Wenn ja, welche Tools wären für welche Aufgaben am ehesten zu empfehlen? 
2) Wie kann ich als deutscher Entwickler dabei die Dsgvo-Richtlinien einalten?
3) Welche Schwachstellen hat dieses Konzept? Welche Probleme könnten sich stellen? 
4) Wie realistisch ist es, eins dieser drei Module im Rahmen des CS50-Abschlussprojekts zu realisieren. Welches Modul käme am ehesten in Frage?  Modul 1wäre mir am liebsten. Aber ich bin auch offen für Modul 2 oder 3. Welches Modul auch immer du empfiehlst: Welche Abstriche müsste ich machen? Worauf müsste ich mich konzentrieren, um eine "minimum viable product" - Version des Moduls zu realisieren?