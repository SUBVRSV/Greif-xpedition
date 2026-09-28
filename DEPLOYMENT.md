# GREIF XPEDITION – Deployment-Anleitung

Stand: September 2026. Alles läuft ohne Server, ohne Datenbank, ohne laufende Kosten. Reine statische Dateien.

## 1. Was gehört auf den Server (Pflicht)

Diese Dateien müssen zusammen in EINEN Ordner (das Web-Wurzelverzeichnis). Sie verlinken sich gegenseitig über relative Pfade, also niemals in Unterordner trennen.

| Datei | Was | Pflicht |
|---|---|---|
| index.html | Das Handbuch (Startseite), 94 Kapitel | ✅ ja |
| buch.html | Das Buch, 10 Kapitel | ✅ ja |
| assistent.html | Der Offline-Krisenberater | ✅ ja |
| sw.js | Service Worker (macht alles offline-fähig) | ✅ ja |
| preview.png | Vorschaubild für Social-Media-Links | ✅ ja |

Das sind die fünf Dateien, die live gehen. Mehr braucht es für die Website nicht.

## 2. Wohin? (drei erprobte Wege)

### A) GitHub Pages (kostenlos, dein bisheriger Weg)
1. Die fünf Dateien ins Repository legen (z. B. subvrsv/Greif-xpedition), in den Wurzelordner oder in /docs.
2. In den Repo-Einstellungen unter "Pages" die Quelle auf diesen Branch/Ordner stellen.
3. Nach ein, zwei Minuten ist alles unter der GitHub-Pages-Adresse live.
Wichtig: preview.png muss im selben Ordner wie index.html liegen, sonst zeigen Social-Media-Vorschauen nichts.

### B) Eigene Domain / Webspace (dein subvrsv.de)
1. Die fünf Dateien per FTP/SFTP ins öffentliche Verzeichnis laden (meist "public_html" oder "htdocs").
2. Fertig. Aufruf über deine Domain.
Der Server sollte HTTPS liefern (fast alle tun das heute automatisch), sonst funktioniert der Service Worker (Offline-Modus) nicht.

### C) Jeder andere Static-Host
Netlify, Cloudflare Pages, Vercel und ähnliche: Ordner mit den fünf Dateien hochladen oder mit dem Repo verbinden. Kein Build nötig, es sind fertige Dateien.

## 3. Nach dem Hochladen: der Cache-Trick

Der Service Worker speichert die Seiten offline. Nach jedem Update musst du den Cache brechen, sonst sehen wiederkehrende Besucher die alte Version. Das ist schon vorbereitet: In sw.js steht oben ein Cache-Name (aktuell "greif-V45.2"). Bei jedem neuen Upload wurde diese Nummer hochgezählt, dadurch lädt der Browser automatisch frisch.
Falls du selbst etwas änderst: die Versionsnummer in sw.js erhöhen, sonst greift der alte Cache.

Für dich zum Testen nach dem Deployment: einmal hart neu laden (Strg+Umschalt+R am Rechner, am Handy Seite schließen und neu öffnen).

## 4. Optional: der KI-Assistent zum Weitergeben (kein Server nötig)

Diese Dateien sind NICHT für die Website, sondern zum Verteilen an Leute, die sich ihren eigenen KI-Berater bauen wollen (z. B. in ChatGPT oder Claude):

| Datei | Zweck |
|---|---|
| wissensbasis-kompakt.md | Das komprimierte Wissen (empfohlen) |
| wissensbasis.json | Der Volltext (für Umgebungen, die viel verarbeiten) |
| systemprompt.md | Die Verhaltens-Anweisung für die KI |
| ANLEITUNG.md | Schritt-für-Schritt-Anleitung (4 Wege) |

Diese vier kannst du als ZIP weitergeben, verlinken oder zum Download anbieten. Sie gehören nicht zwingend auf den Webserver, schaden dort aber auch nicht.

## 5. Optional: Präsentation & interne Dokumente

Nicht für die Öffentlichkeit gedacht, für dich:

| Datei | Zweck |
|---|---|
| pitch.html | Pitch-Infografik (Präsentation, USP auf einen Blick) |
| uebersicht.html | Projekt-Schaubild (Architektur, für dich/Mitwirkende) |
| BRIEFING.md | Technische Projektnotizen für die nächste Arbeitssitzung |
| release_check.py | Prüfskript vor jedem Release (18 Checks) |
| linkrot_check.py | Prüft externe Links auf Erreichbarkeit (lokal ausführen) |

## 6. Schnellste Variante (Minimal-Deployment)

Wenn du JETZT online gehen willst, reicht das:
1. index.html, buch.html, assistent.html, sw.js, preview.png in einen Ordner.
2. Ordner zu GitHub Pages oder deinem Webspace.
3. Aufrufen, hart neu laden, fertig.

## Aktuelle Versionen (Stand dieses Pakets)
- Handbuch (index.html): V45.2
- Buch (buch.html): V3.6
- Assistent (assistent.html): V1.5
- Service Worker (sw.js): greif-V45.2
- Inhaltsstand: September 2026

## Wichtige Hinweise
- Alle Dateien sind reiner HTML/CSS/JS-Text, kein Framework, kein Build.
- Alles funktioniert offline, sobald es einmal geladen wurde (Service Worker).
- Keine Nutzerdaten verlassen das Gerät. Alles läuft im Browser.
- Bei akuter Gefahr verweist der Assistent auf Notruf 112. Das ist so gewollt und sollte so bleiben.
