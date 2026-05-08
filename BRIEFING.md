# GREIF XPEDITION Krisenhandbuch -- Briefing für neuen Chat

## Projekt
Deutsches Krisenvorsorge-Handbuch von @greif_xpedition.
Single-HTML PWA. Gehostet: https://subvrsv.github.io/Greif-xpedition/

## Aktueller Stand
**Version: V38.3** (Mai 2026)
87 Kapitel | 83 Nav-Gruppen-Einträge | 1,58 MB | 7 JS-Blöcke
Alle Tests grün: JS OK, Sections-Reihenfolge OK, Maps synchron, keine Dopplungen, keine Em-Dashes.

## Dateien
- `index.html` -- alles inline (HTML + CSS + JS + base64-Bilder)
- `sw.js` -- Service Worker (Cache-Name muss mit Version sync sein)
- `release_check.py` / `acceptance_test.py` / `test_nav.py`

## Core-Regeln
- Keine Em-Dashes (--), korrekte Umlaute, keine Apostrophe in JS-Kommentaren
- Version +0.01 bei jeder Änderung in 4 Stellen (HTML-Kommentar, Sidebar-Footer, Cover-Meta, Cover-Notice) + sw.js Cache-Name
- JS Syntax-Check: `node --check` auf alle 7 Blöcke nach jeder JS-Änderung
- `python3 release_check.py index.html VNEW VOLD` + `acceptance_test.py` (48/48) + `test_nav.py`

## Sidebar-Gruppen (V38.3)
- **ng-l1:** bug-out-bag, chest-pack, kleidung-ausruestung, tools-hacks, fluessigkeiten-bob
- **ng-l1b:** nahrung-konzept, essensplan, einkaufsliste, nahrung-lagerung, feldkueche, nahrung-naehrstoffe
- **ng-l2:** medizin-erstehilfe, medikamente-vorrat, medizin-ohne-arzt, hygiene-sanitaer, haushalts-ressourcen, kommunikation-krise, navigation-krise, energie-strom, technik-field, finanzen-dokumente, finanzkrise, digitale-vorbereitung, soziales-netzwerk
- **ng-l3:** werkzeug-zuhause, wasservorrat, fahrzeug-krise, mobilitaet-krise, shelter-evakuierung, urban-wohnen, urban-mietwohnung, wohnung-absichern, sicherheit-lager, selbstverteidigung, freie-waffen, wildnis-bushcraft, tiere-fruehwarnung, tarp-aufbau, feuer-bedingungen, signalisierung, anbau-konservierung, langzeitlager, jagd-nahrung, heizung-waerme, saisonale-anpassung, hitzewelle, naturgefahren, krieg-unruhen, abc-schutz, cyberangriff, blackout-stufenplan, blackout-matrix, pandemie-biobedrohung, epidemiologie-krise, recht-krisenfall, drohnen-schutz, familiennotfallplan, alleinstehende-krise
- **ng-alltag:** sanitaer-notfall, brand-notfall, gasaustritt, krisenkueche, ausruestungspflege, bartering, kinder-krise
- **ng-zusatz:** mental-staerke, koerperliche-fitness, schlaf-krise, offline-bibliothek, reparieren-krise, mietrecht-krise, warnmeldungen, desinformation-krise, gefahrenerkennung, infrastruktur-karte, staat-planung, dach-besonderheiten, ernaehrungs-biochemie, typische-fehler, budget-krisenvorsorge, szenarien
- **ng-anhang:** quellen, shops
- **Top-Level (keine Gruppe):** cover, inhalt, checklist, krisenkalender

## JS-Blöcke (7 Stück -- alle müssen fehlerfrei sein)
- Block 0: Theme-Init (138 Zeichen)
- Block 1: Theme-Init 2 (149 Zeichen)
- Block 2: Quickdecider-Daten (~9k Zeichen)
- Block 3: Vorratsplaner (~7k Zeichen)
- Block 4: Haupt-JS (~74k Zeichen) -- navTo, const map, _navGroupMap, alle Kernfunktionen
- Block 5: PWA Service Worker Registration (~2k Zeichen)
- Block 6: Online-Status + KPG + Fortschritt (~5k Zeichen)

## Kritische Architektur
- **Zwei Maps SYNCHRON:** `const map` und `const _navGroupMap` (beide in Block 4) -- 83 Einträge je
- **HTML-Reihenfolge = Sidebar-Reihenfolge** (KRITISCH -- sonst Nav-Sprung beim Scrollen)
- **Sidebar ist position:fixed** -- bleibt dunkel auch im Light-Mode (bewusst)
- **Nav-Algorithmus:** größter sichtbarer Flächenanteil im oberen 2/3 des Viewports
- **Sidebar-Scroll:** sidebar.scrollTop (KEIN scrollIntoView -- scrollt sonst die ganze Seite)

## Cover-Struktur (V38.3 -- NICHT MEHR ANFASSEN)
Das Cover hat eine fragile HTML-Struktur. Elemente landen leicht in der Sidebar.
Aktueller Stand: Logo + Titel + Claim + USP-Block (4 Zeilen) + cover-update-notice + Akkordeons
Changelog-Block entfernt. persona-start entfernt. Level-Zeile entfernt.

## Bekannte Fallen
- USP-Block im Cover wandert leicht in die Sidebar -- nach jeder Cover-Änderung prüfen
- scrollIntoView() NICHT in _updateActiveNav verwenden -- scrollt die ganze Seite
- JS-Strings mit HTML-Inhalt: doppelte Quotes verwenden (keine einfachen -- Syntaxfehler)
- Orphaned JS-Blöcke nach Umstrukturierungen immer node --check prüfen
- HTML-Reihenfolge nach Sections-Umordnung mit test_nav.py verifizieren

## Features (V38.3)
- Neue Suche: Kapitel / Auch erwähnt in Trennung, Volltext ab 3 Zeichen
- Fortschrittsanzeige Sidebar (X von 81 Kapiteln gelesen)
- Krisenplan-Generator (8 Fragen, 3 Prioritätsstufen)
- DACH-Besonderheiten Kapitel
- PTSD & Trauma-Nachsorge in mental-staerke
- 30 kuratierte Quellen mit Kommentar
- Preise recherchiert Mai 2026

## Preise (Mai 2026 -- nächste Prüfung Nov 2026)
Silber 1 oz: 90-110 EUR | Gold 1 oz: 2.900-3.200 EUR
Sawyer Mini: 35-55 EUR | Leatherman Signal: 120-160 EUR
Morakniv Garberg: 75-105 EUR | GRAYL Ultrapress: 85-110 EUR
EcoFlow River 2 Max: 300-400 EUR | Carinthia Defence 4: 180-250 EUR

## Offene Punkte
- Linkrot-Check lokal: `python3 linkrot_check.py index.html`
- Druck-Test: PDF aus Chrome

## NICHT MEHR ANFASSEN
- Cover-Struktur (zu fragil)
- Light-Mode CSS (Sidebar bleibt dunkel -- bewusst)
- Nav-Algorithmus (stabil seit V36.5)
