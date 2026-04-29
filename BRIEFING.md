# GREIF XPEDITION Krisenhandbuch — Briefing für neuen Chat

## Projekt-Übersicht
Deutsches Krisenvorsorge-Handbuch „GREIF XPEDITION Krisenhandbuch" von @greif_xpedition.
Single-HTML PWA, 84 Kapitel, 416+ Tabellen, ~95k Wörter.
Gehostet auf: https://subvrsv.github.io/Greif-xpedition/
Redirect von: https://greif-xpedition.subvrsv.de/ (SSL-Problem, siehe ssl-fix-notiz.md)

## Aktueller Stand
**Version: V30.4** (Apr 2026)
**Dateigröße:** 1.459 MB
**Release-Check:** 25/25 grün
**Akzeptanz-Test:** 48/48 grün

## Dateien
- `index.html` — Haupt-Datei (alles inline: HTML + CSS + JS + base64-Bilder)
- `sw.js` — Service Worker (Stale-While-Revalidate, Cache-Name muss mit Version sync sein)
- `release_check.py` — Versions-Check vor jedem Release
- `acceptance_test.py` — 48 automatische Tests
- `linkrot_check.py` — Prüft alle 123 externen Links (lokal ausführen, nicht im Container)
- `ssl-fix-notiz.md` — Anleitung SSL-Fix über Cloudflare

## Core-Regeln (IMMER EINHALTEN)
- Keine Em-Dashes (—), stattdessen Punkt/Komma/Doppelpunkt
- Version +0.01 bei jeder Änderung, sw.js Cache-Name synchron halten
- Umlaute korrekt (ä/ö/ü/Ä/Ö/Ü/ß), niemals ae/oe/ue/ss
- Changelog bei jedem Release aktualisieren
- Keine Apostrophe in JS-Kommentaren (Scanner-Bug)
- Light Mode Default: `<body class="light-mode">` direkt im HTML
- Alle Produktempfehlungen mit „z.B." prefixen
- Kein Verweis auf KI-Tooling, kein echter Name des Autors
- `python3 release_check.py index.html VNEW VOLD` vor jedem Release
- `python3 acceptance_test.py index.html` muss 48/48 grün sein

## Release-Workflow
```bash
# 1. Änderungen machen
# 2. Version in 4 Stellen updaten:
#    - HTML-Kommentar oben
#    - Sidebar-Footer "Survival & Krisenvorsorge VX.X"
#    - Cover-Meta "VX.X // GREIF XPEDITION Krisenhandbuch"
#    - Cover-Notice "VX.X: 84 Kapitel..."
# 3. sw.js Cache-Name updaten: const CACHE = 'greif-VX.X';
# 4. Changelog-Eintrag schreiben
# 5. release_check.py + acceptance_test.py — beide grün
# 6. Files nach /mnt/user-data/outputs/ kopieren
# 7. present_files aufrufen
```

## Versions-Chronologie (kompakt)
- V27.x: Mobile-UX, Bookmarks, Resume-Banner, Persona-Karten, Read-Tracking
- V28.x: Print-CSS, Service Worker, Keyboard-Shortcuts, SEO/OG-Tags, Werte-Manifest, Schriftgröße-Toggle, Stand-Markierungen Apr 2026
- V29.0: Reading-Progress, Mini-Header, Resume-Banner entfernt (störten)
- V29.1: Schriftgröße-Toggle repariert (CSS zoom auf #main)
- V29.2: Quellen-System (15 Einträge, 14 verlinkt), Accessibility (aria, Skip-Link), Pandemie-Typen-Tabelle
- V29.3: Tag-Filter entfernt, Release-Check Pingpong gefixt (Changelog-Bereich ausgenommen)
- V29.4: Mobile-Topbar entfernt, floating Burger zurück
- V29.5: Doppel-Burger-Bug gefixt (700-1024px Breakpoint)
- V29.6: Goldener Cover-Strich entfernt, Padding reduziert
- V29.7: Cover-Logo unter Burger verschoben
- V29.8: Suchergebnis-Snippets verbessert, Vor/Nächstes markanter, Sidebar Tab-Fix, 6 weitere Quellen
- V29.9: Manifest-Text entschärft (kein "Mittelstand"), Auslandskonto+Wise-Block, Suchschrift größer, FontSize auch auf Sidebar
- V30.0: Community-Tipp Badge (grün, für Leser-Feedback-Abschnitte)
- V30.1: warn-box CSS-Bug gefixt (hatte kein Styling), alle Boxen kompakter
- V30.2: body-text max-width erhöht, tbody-td in Sans-Schrift
- V30.3: body-text width:100% explicit, max-width entfernt
- V30.4: [aktuell — was hier steht prüfen im Changelog]

## Architektur
- Single HTML, alles inline (~95 KB JS, ~56 KB CSS, ~87 KB base64-Bilder)
- localStorage-Keys: theme, readSections, bookmarks, kk* (Krisenkalender), wfm* (Was-fehlt), szpDone, szpCurrent, fontsize, personaOpen
- Zwei JS-Maps müssen synchron sein: `const map = {...}` und `const _navGroupMap = {...}`
  - Beide mappen Section-IDs auf Sidebar-Gruppen (ng-l1, ng-l1b, ng-l2, ng-l3, ng-alltag, ng-zusatz, ng-anhang)
  - Top-Level (keine Gruppe): einstieg-accordion, checklist, cover, krisenkalender
- FontSize-Toggle: CSS zoom auf #main UND #sidebar (A+=1.12, A++=1.25), Firefox-Fallback mit font-size
- Service Worker: Stale-While-Revalidate, Cache-Name muss mit Version übereinstimmen

## Kritische JS-Funktionen (dürfen nicht fehlen)
navTo, navSearch, buildSearchIndex, openTool, printSection, doPrint,
szpShow, szpBannerUpdate, szpBannerNav, szpBannerClose, szpReset, szpSave, szpLoad,
wfmRender, wfmInit, wfmSave, wfmToggle, wfmReset,
kkInit, kkRenderNav, kkRenderMonth, kkSave,
toggleSidebar, _injectChapterNav, _updateReadingUx, _markSectionRead, _initReadMarkers,
toggleBookmark, _injectBookmarkButtons, _refreshBookmarkUI, favClick,
_setupExternalLinks, toggleFontSize, _initFontSize, toggleGroup, _initNavGroupAria,
accToggle, _updateActiveNav

## Sidebar-Gruppen-Struktur
- ng-l1: Bug-Out-Bag, Chest-Pack, Kleidung, Tools, Flüssigkeiten
- ng-l1b: Nahrung-Konzept, Essensplan, Nahrung-Langzeit, Wasservorrat
- ng-l2: Medizin, Kommunikation, Energie, Navigation, Hygiene, Finanzen, Psychologie
- ng-l3: Fahrzeug, Langzeit-Wasser, Sicherheit, Anbau, Heizung, Hitzewelle, Naturgefahren, Jagd, Basislager, ABC-Schutz, Krieg, Recht
- ng-alltag: Urban, Familie, Haustiere, Alltags-EDC
- ng-zusatz: Digitale-Vorbereitung, Kühlkette, Autarkie, Szenariopfade
- ng-anhang: Quellen, Changelog, Inhalt

## Design-Entscheidungen (bewusst so, nicht ändern)
- Mono-Font (IBM Plex Mono), Amber auf Dunkel, Militär-Ästhetik — das ist Absicht, nicht Fehler
- Der Autor will es NICHT massentauglicher gestalten, der Charakter soll bleiben
- Warn-Boxen: warn-box und warning-box sind identisch gestylt (beide existieren im HTML)
- Community-Tipp Badge: grünes `<span class="community-badge">Community-Tipp</span>` für Leser-Feedback-Abschnitte
- tbody-td: Sans-Schrift für bessere Lesbarkeit bei Text-Tabellen, erste Spalte bleibt Mono

## Quellen-System
15 Quellen (q1-q15) in der Quellen-Section als `<tr id="qX" class="cite-target">`.
14 davon im Fließtext verlinkt mit `<sup class="cite"><a href="#qX">[X]</a></sup>`.
q3 (SAIDI/Bundesnetzagentur) hat keinen passenden Fließtext-Anker.
Verwendete Quellen: Robine 2003 Hitzetote, RKI 2022 Hitzetote, Bundesnetzagentur SAIDI,
ENTSO-E Iberian Blackout, BBK 10-Tage, Vogel Medizin, Bergrettung Tirol Lawine,
WHO Influenza, Saurugg Blackout, BfArM MHD, DLRG Eis, BKA Cyber, UBA Wasser,
RKI Quarantäne, StGB §32 Notwehr.

## Accessibility-Stand
- Skip-Link „Zum Hauptinhalt springen" (oben, unsichtbar bis Tab-Fokus)
- aria-label auf: Sidebar, Search, Menu-Toggle, Main, FontSize-Toggle-Group, alle Buttons
- Nav-Group-Header: role=button, tabindex=0, aria-expanded, Enter/Space bedienbar
- Bookmark-Sterne: aria-label, aria-pressed
- Sidebar auf Mobile: visibility:hidden wenn geschlossen (kein Tab-Fokusfallen)

## Offen / Nächste Schritte
1. SSL-Fix: Cloudflare einrichten für greif-xpedition.subvrsv.de (siehe ssl-fix-notiz.md)
2. Linkrot-Checker lokal ausführen: `python3 linkrot_check.py index.html`
3. Druck-Test: Als PDF aus Chrome drucken und durchblättern
4. Weitere Community-Tipp Badges wenn Leser-Feedback kommt
5. Weitere Quellen im Fließtext wenn neue Behauptungen hinzukommen

## Netzwerk-Hinweis für Container
Externe Domains sind im Claude-Container gesperrt (außer api.anthropic.com, github.com, pypi.org etc.).
linkrot_check.py muss lokal ausgeführt werden, nicht im Container.
