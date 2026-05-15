# GREIF XPEDITION Krisenhandbuch -- Briefing für neuen Chat

## Projekt
Deutsches Krisenvorsorge-Handbuch von @greif_xpedition.
Single-HTML PWA. Gehostet: https://subvrsv.github.io/Greif-xpedition/

## Aktueller Stand
**Version: V39.4** (Mai 2026)
87 Kapitel | 1,72 MB | 7 JS-Blöcke | 118.000 Wörter
Alle Tests grün: 47/48 (Persona-Karten absichtlich entfernt), Nav OK (333 IDs, 86 Sidebar-Links, 9 Gruppen), keine Em-Dashes, alle Stände auf Mai 2026.

## Dateien
- `index.html` -- alles inline (HTML + CSS + JS + base64-Bilder)
- `sw.js` -- Service Worker (Cache-Name: greif-V39.4 -- synchron mit HTML)
- `acceptance_test.py` / `test_nav.py` -- Testreihe (47/48 + Nav OK)
- `linkrot_check.py` -- Linkrot-Checker (DNS-Fehler vs. Bot-Block-Erkennung, Unicode-URLs)

## Core-Regeln
- Keine Em-Dashes (--), korrekte Umlaute, keine Apostrophe in JS-Kommentaren
- Version +0.1 bei jeder Änderung in 4 Stellen (HTML-Kommentar, Sidebar-Footer, Cover-Meta, Cover-Notice) + sw.js Cache-Name
- JS Syntax-Check: `node --check` auf alle 7 Blöcke nach jeder JS-Änderung
- `acceptance_test.py` (47/48) + `test_nav.py` (Nav OK) nach jeder Änderung
- Immer BEIDE Dateien ausgeben: index.html + sw.js
- Stand-Datum in Section-Banner bei inhaltlichen Änderungen auf aktuelles Datum setzen

## Sidebar-Gruppen (V39.1 -- unverändert seit V38.5)
- **ng-l1:** bug-out-bag, chest-pack, kleidung-ausruestung, tools-hacks, fluessigkeiten-bob
- **ng-l1b:** nahrung-konzept, essensplan, einkaufsliste, nahrung-lagerung, feldkueche, nahrung-naehrstoffe
- **ng-l2:** medizin-erstehilfe, medikamente-vorrat, medizin-ohne-arzt, hygiene-sanitaer, haushalts-ressourcen, kommunikation-krise, navigation-krise, energie-strom, technik-field, finanzen-dokumente, finanzkrise, digitale-vorbereitung, soziales-netzwerk, werkzeug-zuhause
- **ng-l3a (Wohnen & Sicherheit):** werkzeug-zuhause, wasservorrat, fahrzeug-krise, mobilitaet-krise, shelter-evakuierung, urban-wohnen, urban-mietwohnung, wohnung-absichern, sicherheit-lager, selbstverteidigung, freie-waffen
- **ng-l3b (Wildnis & Versorgung):** wildnis-bushcraft, tiere-fruehwarnung, tarp-aufbau, feuer-bedingungen, signalisierung, anbau-konservierung, langzeitlager, jagd-nahrung, heizung-waerme, saisonale-anpassung
- **ng-l3c (Krisen & Bedrohungen):** hitzewelle, naturgefahren, krieg-unruhen, abc-schutz, cyberangriff, blackout-stufenplan, blackout-matrix, pandemie-biobedrohung, epidemiologie-krise, recht-krisenfall, drohnen-schutz, familiennotfallplan, alleinstehende-krise
- **ng-alltag:** sanitaer-notfall, brand-notfall, gasaustritt, krisenkueche, ausruestungspflege, bartering, kinder-krise
- **ng-zusatz:** mental-staerke, koerperliche-fitness, schlaf-krise, offline-bibliothek, reparieren-krise, mietrecht-krise, warnmeldungen, desinformation-krise, gefahrenerkennung, infrastruktur-karte, staat-planung, dach-besonderheiten, ernaehrungs-biochemie, typische-fehler, budget-krisenvorsorge, szenarien
- **ng-anhang:** quellen, shops
- **Top-Level (keine Gruppe):** cover, inhalt, checklist, krisenkalender

## JS-Blöcke (7 Stück -- alle müssen fehlerfrei sein)
- Block 0: Theme-Init (138 Zeichen)
- Block 1: Theme-Init 2 (149 Zeichen)
- Block 2: Quickdecider-Daten (~11k Zeichen) -- 9 Szenarien inkl. "unterwegs"
- Block 3: Vorratsplaner (~8k Zeichen)
- Block 4: Haupt-JS (~80k Zeichen) -- navTo, const map, _navGroupMap, alle Kernfunktionen
- Block 5: PWA Service Worker Registration (~2k Zeichen)
- Block 6: Online-Status + KPG + Fortschritt (~6k Zeichen)

## Kritische Architektur
- **Drei Maps SYNCHRON:** `const map` und `const _navGroupMap` (beide in Block 4) -- ng-l3 ist aufgeteilt in ng-l3a/b/c
- **HTML-Reihenfolge = Sidebar-Reihenfolge** (KRITISCH -- sonst Nav-Sprung beim Scrollen)
- **Sidebar ist position:fixed** -- bleibt dunkel auch im Light-Mode (bewusst)
- **Nav-Algorithmus:** größter sichtbarer Flächenanteil im oberen 2/3 des Viewports
- **Sidebar-Scroll:** sidebar.scrollTop (KEIN scrollIntoView -- scrollt sonst die ganze Seite)
- **Akkordeon-Handler:** document.addEventListener('click') auf [data-acc] -- KEIN zusätzlicher Handler nötig
- **Sidebar-Scrollbar:** ausgeblendet via scrollbar-width:none + ::-webkit-scrollbar {display:none}
- **chapter-nav-box:** Sprungnavigation innerhalb langer Kapitel -- IDs auf subsection-divs setzen

## Schrift / Tabellen (unverändert seit V38.5)
- `tbody td`: Sans 14px
- `tbody td:first-child`: Sans 14px (kein Mono, kein fett)
- `.nav-link`: 15px
- `.body-text`: 15px
- Sidebar bleibt Mono (nav-links, badges, meta)

## Cover-Struktur (NICHT MEHR ANFASSEN)
Das Cover hat eine fragile HTML-Struktur. Elemente landen leicht in der Sidebar.
Akkordeon-Tabs: Notfall-Übersicht, Schnellentscheider, Mein Krisenplan, Vorratsplaner, Erste 10 Minuten, Was fehlt mir noch?, Szenariopfade, Einstieg & FAQ

## Bekannte Fallen
- USP-Block im Cover wandert leicht in die Sidebar -- nach jeder Cover-Änderung prüfen
- scrollIntoView() NICHT in _updateActiveNav verwenden -- scrollt die ganze Seite
- JS-Strings mit HTML-Inhalt: doppelte Quotes verwenden (keine einfachen -- Syntaxfehler)
- Orphaned JS-Blöcke nach Umstrukturierungen immer node --check prüfen
- HTML-Reihenfolge nach Sections-Umordnung mit test_nav.py verifizieren
- navigateTo() existiert NICHT -- immer navTo() verwenden
- Beide JS-Maps (const map + const _navGroupMap) müssen synchron bleiben wenn Gruppen geändert werden
- box-shadow auf overflow-y:auto Elementen wird von Chrome abgeschnitten -- nicht verwenden
- chapter-nav-box Anker-IDs müssen auf div/h3 im selben Chapter gesetzt werden (nicht auf andere Sections)

## Features (V39.1 -- vollständige Liste)
- Schnellentscheider: 9 Szenarien inkl. "Ich bin unterwegs" (Auto/Öffis ausgefallen)
- Ampel-Stufenplan (Grün/Gelb/Orange/Rot) in shelter-evakuierung + familiennotfallplan
- OsmAnd GPX-Tutorial (7 Schritte) in navigation-krise
- Offline-Karten-Abschnitt (OsmAnd, Maps.me, Google, Garmin) in navigation-krise
- "Zu Fuß durch die Stadt" als 6. Akkordeon in mobilitaet-krise
- Fahrrad-Reparatur (Platten, Kette, Bremse, Schaltung) in mobilitaet-krise
- Nahrung ohne Kochen (10 Optionen, 24h-BOB-Ration) in feldkueche
- Kaliumiodid-Protokoll (Dosis, Altersgruppen, Kontraindikationen) in abc-schutz
- Babys & Kleinkinder komplett (Stillen, Windeln, Wärme, Baby-BOB) in kinder-krise
- KI-Desinformation (Deepfakes, Audiofakes, Verifikations-Workflow) in desinformation-krise
- Alleinstehende: Stufenplan + Psychologie + Familienvergleich in alleinstehende-krise
- Budget: Preise Mai 2026 + Einkaufsquellen-Tabelle in budget-krisenvorsorge
- Nav-Boxen in 8 grossen Kapiteln ohne Sprungnavigation (mobilitaet-krise, energie-strom, kommunikation-krise, navigation-krise, fahrzeug-krise, urban-mietwohnung, tools-hacks, fluessigkeiten-bob)
- Tarp-Aufbau: A-Frame Schritt-für-Schritt, Lagerplatz wählen, Fehler-Tabelle
- Feuer: 5 Holzkategorien, 4 Aufbautypen, Feuer im Winter
- Read-Times für 15 Kapitel korrigiert
- Bugfix: 8 kaputte Weiterführend-Links im Schnellentscheider (l2-energie -> energie-strom, l3-shelter -> shelter-evakuierung, ch08 -> bug-out-bag etc.)
- Alle 87 Kapitel auf Stand Mai 2026
- linkrot_check.py: Linkrot-Checker mit Bot-Block-Erkennung
- Suche: Kapitel / Auch erwähnt in Trennung, Volltext ab 3 Zeichen
- Fortschrittsanzeige Sidebar (X von 81 Kapiteln gelesen)
- Krisenplan-Generator (8 Fragen, 3 Prioritätsstufen)
- SW Update-Banner (kein harter Reload)
- Print-CSS: Akkordeons aufgeklappt

## Preise (Mai 2026 -- nächste Prüfung Nov 2026)
Silber 1 oz: 90-110 EUR | Gold 1 oz: 2.900-3.200 EUR
Sawyer Mini: 35-55 EUR | Leatherman Signal: 120-160 EUR
Morakniv Garberg: 75-105 EUR | GRAYL Ultrapress: 85-110 EUR
EcoFlow River 2 Max: 300-400 EUR | Carinthia Defence 4: 180-250 EUR

## Offene Punkte (nächste Session -- V39.2)
- Keine bekannten inhaltlichen Lücken
- Bugfix V39.2: 8 kaputte Weiterführend-Links im Schnellentscheider repariert (l2-energie, l3-shelter, ch08 etc.)
- Linkrot-Check mit `python3 linkrot_check.py index.html --only-errors` auf eigenem Rechner durchführen (DNS war in Sandbox blockiert)
- Druck-Test: PDF aus Chrome (Print-CSS vorhanden, noch nicht verifiziert)
- Preise November 2026 prüfen

## NICHT MEHR ANFASSEN
- Cover-Struktur (zu fragil)
- Light-Mode CSS (Sidebar bleibt dunkel -- bewusst)
- Nav-Algorithmus (stabil seit V36.5)
- Akkordeon-Handler (funktioniert via document click auf [data-acc])
- Sidebar-Scrollbar (ausgeblendet -- bewusst, sieht sonst aus wie defekter Strich)
- Sidebar-Gruppen und JS-Maps (synchron und stabil -- nur ändern wenn neue Kapitel/Gruppen)
