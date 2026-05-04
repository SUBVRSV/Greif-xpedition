# GREIF XPEDITION Krisenhandbuch — Briefing für neuen Chat

## Projekt-Übersicht
Deutsches Krisenvorsorge-Handbuch von @greif_xpedition.
Single-HTML PWA, 86 Kapitel, 459+ Tabellen, ~98k Wörter.
Gehostet auf: https://subvrsv.github.io/Greif-xpedition/
(Direkt GitHub Pages -- kein Redirect, kein SSL-Problem)

## Aktueller Stand
**Version: V32.3** (Apr 2026)
**Dateigröße:** 1,52 MB
**Release-Check:** 25/25 grün
**Akzeptanz-Test:** 48/48 grün
**Titel:** "Wahrscheinlich das umfangreichste kostenlose deutschsprachige Handbuch zu Survival & Krisenvorsorge"

## Dateien
- `index.html` — Haupt-Datei (alles inline: HTML + CSS + JS + base64-Bilder)
- `sw.js` — Service Worker (Stale-While-Revalidate, Cache-Name muss mit Version sync sein)
- `release_check.py` — Versions-Check vor jedem Release
- `acceptance_test.py` — 48 automatische Tests
- `test_nav.py` — Nav-Simulator (prüft Sidebar-IDs, navTo, JS-Maps)
- `linkrot_check.py` — Prüft externe Links (lokal ausführen, nicht im Container)

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
- `python3 test_nav.py index.html` muss grün sein

## Release-Workflow
```bash
# 1. Änderungen machen
# 2. Version in 4 Stellen updaten:
#    - HTML-Kommentar oben
#    - Sidebar-Footer "Survival & Krisenvorsorge VX.X"
#    - Cover-Meta "VX.X // GREIF XPEDITION Krisenhandbuch"
#    - Cover-Notice "VX.X: 86 Kapitel..."
# 3. sw.js Cache-Name updaten: const CACHE = 'greif-VX.X';
# 4. Changelog-Eintrag schreiben
# 5. release_check.py + acceptance_test.py + test_nav.py — alle grün
# 6. Files nach /mnt/user-data/outputs/ kopieren
# 7. present_files aufrufen
```

## Architektur
- Single HTML, alles inline (~95 KB JS, ~56 KB CSS, ~87 KB base64-Bilder)
- localStorage-Keys: theme, personaOpen (weitere: readSections, bookmarks, kk*, wfm*, szpDone, szpCurrent, fontsize)
- Zwei JS-Maps müssen synchron sein: `const map = {...}` und `const _navGroupMap = {...}`
  - Beide mappen Section-IDs auf Sidebar-Gruppen
  - Top-Level (keine Gruppe): cover, einstieg-accordion, checklist, krisenkalender, was-fehlt, szenariopfade
- FontSize-Toggle: CSS zoom auf #main UND #sidebar (A+=1.12, A++=1.25), Firefox-Fallback mit font-size
- Service Worker: Stale-While-Revalidate, Cache-Name muss mit Version übereinstimmen

## Sidebar-Gruppen-Struktur (V32.3)
- **ng-l1:** bug-out-bag, chest-pack, kleidung-ausruestung, tools-hacks, fluessigkeiten-bob
- **ng-l1b:** nahrung-konzept, essensplan, einkaufsliste, nahrung-lagerung, feldkueche, nahrung-naehrstoffe
- **ng-l2:** medizin-erstehilfe, medikamente-vorrat, medizin-ohne-arzt, hygiene-sanitaer, haushalts-ressourcen, kommunikation-krise, navigation-krise, energie-strom, technik-field, finanzen-dokumente, finanzkrise, digitale-vorbereitung, soziales-netzwerk
- **ng-l3:** werkzeug-zuhause, wasservorrat, fahrzeug-krise, mobilitaet-krise, shelter-evakuierung, urban-wohnen, urban-mietwohnung, wohnung-absichern, sicherheit-lager, selbstverteidigung, freie-waffen, wildnis-bushcraft, tiere-fruehwarnung, tarp-aufbau, feuer-bedingungen, signalisierung, anbau-konservierung, langzeitlager, jagd-nahrung, heizung-waerme, saisonale-anpassung, hitzewelle, naturgefahren, krieg-unruhen, abc-schutz, cyberangriff, blackout-stufenplan, blackout-matrix, pandemie-biobedrohung, epidemiologie-krise, recht-krisenfall, drohnen-schutz, familiennotfallplan, alleinstehende-krise
- **ng-alltag:** sanitaer-notfall, brand-notfall, gasaustritt, krisenkueche, ausruestungspflege, bartering, kinder-krise
- **ng-zusatz:** mental-staerke, koerperliche-fitness, schlaf-krise, offline-bibliothek, reparieren-krise, mietrecht-krise, warnmeldungen, desinformation-krise, gefahrenerkennung, infrastruktur-karte, staat-planung, ernaehrungs-biochemie, typische-fehler, budget-krisenvorsorge, szenarien
- **ng-anhang:** quellen, shops

## Kritische JS-Funktionen (dürfen nicht fehlen)
navTo, navSearch, buildSearchIndex, openTool, printSection, doPrint,
szpShow, szpBannerUpdate, szpBannerNav, szpBannerClose, szpReset, szpSave, szpLoad,
wfmRender, wfmInit, wfmSave, wfmToggle, wfmReset,
kkInit, kkRenderNav, kkRenderMonth, kkSave,
toggleSidebar, _injectChapterNav, _updateReadingUx, _markSectionRead, _initReadMarkers,
toggleBookmark, _injectBookmarkButtons, _refreshBookmarkUI, favClick,
_setupExternalLinks, toggleFontSize, _initFontSize, toggleGroup, _initNavGroupAria,
accToggle, _updateActiveNav

## Design-Entscheidungen (bewusst so, nicht ändern)
- Mono-Font (IBM Plex Mono), Amber auf Dunkel, Militär-Ästhetik -- Absicht, kein Fehler
- Autor will NICHT massentauglicher gestalten, Charakter bleibt
- warn-box und warning-box sind identisch gestylt (beide existieren im HTML)
- Community-Tipp Badge: grünes `<span class="community-badge">Community-Tipp</span>`
- tbody-td: Sans-Schrift für Text-Tabellen, erste Spalte bleibt Mono
- H3-CSS: Amber-Akzentlinie, unterscheidet sich sauber von .subsection
- Rhetorische Kurzsätze (Dreier-Betonung, Pointen) sind Stilmittel -- nicht anfassen

## Quellen-System
15 Quellen (q1-q15) in der Quellen-Section als `<tr id="qX" class="cite-target">`.
14 davon im Fließtext verlinkt mit `<sup class="cite"><a href="#qX">[X]</a></sup>`.

## Accessibility-Stand
- Skip-Link "Zum Hauptinhalt springen" (oben, unsichtbar bis Tab-Fokus)
- aria-label auf: Sidebar, Search, Menu-Toggle, Main, FontSize-Toggle-Group, alle Buttons
- Nav-Group-Header: role=button, tabindex=0, aria-expanded, Enter/Space bedienbar
- Sidebar auf Mobile: visibility:hidden wenn geschlossen

## Was in dieser Chat-Session erarbeitet wurde (V30.4 -> V32.3)
Über 60 neue Blöcke und Kapitel, inkl.:
- h3-Gliederung in allen langen Kapiteln
- 5 komplett neue Kapitel (medikamente-vorrat, alleinstehende-krise, budget-krisenvorsorge, infrastruktur-karte, medizin-ohne-arzt erweitert)
- Todesordner, Krisengruppe, Haltbarmachung, Brot ohne Strom, Spezialdiäten
- EMP-Schutz, Hochwasser, Datenprepping, Fahrzeug-Panne, Kleintierzucht
- Satellitenkommunikation, Wasseraufbereitung Stufe 2, Erfrierung/Unterkühlung
- Impfschutz/Tetanus, Edelmetalle, Wasserweg/Kanu, Wind/Wasserkraft
- Extrembedrohung/Geiselnahme, Fremde an der Tür
- Großer Strukturumbau V32.0: Kapitel neu gruppiert, Anhang aufgeräumt
- Dopplungsbereinigung (Zahn, Verbrennung, urban-Lagerung)
- Rechtschreib- und Sprachdurchlauf

## Offen / Nächste Schritte
1. PTSD & Trauma-Nachsorge (bewusst zurückgestellt)
2. Linkrot-Checker lokal ausführen: `python3 linkrot_check.py index.html`
3. Druck-Test: Als PDF aus Chrome drucken und durchblättern

## Netzwerk-Hinweis für Container
Externe Domains sind im Claude-Container gesperrt (außer api.anthropic.com, github.com, pypi.org etc.).
linkrot_check.py muss lokal ausgeführt werden, nicht im Container.
