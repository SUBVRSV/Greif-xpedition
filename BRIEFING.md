# GREIF XPEDITION Krisenhandbuch -- Briefing für neuen Chat

## Projekt-Übersicht
Deutsches Krisenvorsorge-Handbuch von @greif_xpedition.
Single-HTML PWA, 87 Kapitel, 465 Tabellen, ~100.000 Wörter, 1,56 MB.
Gehostet auf: https://subvrsv.github.io/Greif-xpedition/
(Direkt GitHub Pages -- kein Redirect, kein SSL-Problem, anonym)
Claim: "Wahrscheinlich das umfangreichste kostenlose deutschsprachige Handbuch zu Survival & Krisenvorsorge"

## Aktueller Stand
**Version: V34.3** (Mai 2026)
**Release-Check:** 25/25 grün | **Akzeptanz-Test:** 48/48 grün
**Nav-Simulator:** OK (286 IDs, 89 Sidebar-Links, 7 Gruppen)
**JS-Syntax:** Alle 7 Blöcke fehlerfrei | **Em-Dashes:** 0

## Dateien
- `index.html` -- Haupt-Datei (alles inline: HTML + CSS + JS + base64-Bilder)
- `sw.js` -- Service Worker (Cache-Name muss mit Version sync sein)
- `release_check.py` / `acceptance_test.py` / `test_nav.py`
- `linkrot_check.py` -- nur lokal ausfuehren

## Core-Regeln (IMMER)
- Keine Em-Dashes (--), korrekte Umlaute (ä/ö/ü/ß), keine Apostrophe in JS-Kommentaren
- Version +0.01 bei jeder Änderung in 4 Stellen: HTML-Kommentar, Sidebar-Footer, Cover-Meta, Cover-Notice
- sw.js Cache-Name synchron: `const CACHE = 'greif-VX.X'`
- Alle Produktempfehlungen mit "z.B." prefixen
- JS Syntax-Check nach jeder JS-Änderung: alle 7 Blöcke mit `node --check`
- `python3 release_check.py index.html VNEW VOLD` + `acceptance_test.py` (48/48) + `test_nav.py`

## Kritische Architektur

### JS-Blöcke (7 Stück)
Block 4 (~74.500 Zeichen) ist der Haupt-Block mit navTo, const map, _navGroupMap und allen Kernfunktionen.
Block 6 (~5.500 Zeichen) hat KPG, Fortschrittsanzeige, Online-Status.

### Zwei Maps SYNCHRON halten (beide in Block 4)
```js
const map = { 'section-id': 'ng-gruppe', ... }
const _navGroupMap = { 'section-id': 'ng-gruppe', ... }
```
Neue Section: BEIDE Maps + Sidebar-Link.

### HTML-Reihenfolge = Sidebar-Reihenfolge (KRITISCH)
Sections im HTML muessen in der gleichen Reihenfolge stehen wie in der Sidebar.
Falsche Reihenfolge = Nav-Sprung beim Scrollen. Behoben in V33.8.

### JS-Syntax-Fallen
- Kein `'` in JS-Strings mit HTML-Inhalt (z.B. onclick-Attribute) -- doppelte Quotes verwenden
- Keine orphaned Codeblöcke nach Umstrukturierungen -- immer alle 7 Blöcke pruefen

## Sidebar-Gruppen (V34.3)
- **ng-l1:** bug-out-bag, chest-pack, kleidung-ausruestung, tools-hacks, fluessigkeiten-bob
- **ng-l1b:** nahrung-konzept, essensplan, einkaufsliste, nahrung-lagerung, feldkueche, nahrung-naehrstoffe
- **ng-l2:** medizin-erstehilfe, medikamente-vorrat, medizin-ohne-arzt, hygiene-sanitaer, haushalts-ressourcen, kommunikation-krise, navigation-krise, energie-strom, technik-field, finanzen-dokumente, finanzkrise, digitale-vorbereitung, soziales-netzwerk
- **ng-l3:** werkzeug-zuhause, wasservorrat, fahrzeug-krise, mobilitaet-krise, shelter-evakuierung, urban-wohnen, urban-mietwohnung, wohnung-absichern, sicherheit-lager, selbstverteidigung, freie-waffen, wildnis-bushcraft, tiere-fruehwarnung, tarp-aufbau, feuer-bedingungen, signalisierung, anbau-konservierung, langzeitlager, jagd-nahrung, heizung-waerme, saisonale-anpassung, hitzewelle, naturgefahren, krieg-unruhen, abc-schutz, cyberangriff, blackout-stufenplan, blackout-matrix, pandemie-biobedrohung, epidemiologie-krise, recht-krisenfall, drohnen-schutz, familiennotfallplan, alleinstehende-krise
- **ng-alltag:** sanitaer-notfall, brand-notfall, gasaustritt, krisenkueche, ausruestungspflege, bartering, kinder-krise
- **ng-zusatz:** mental-staerke, koerperliche-fitness, schlaf-krise, offline-bibliothek, reparieren-krise, mietrecht-krise, warnmeldungen, desinformation-krise, gefahrenerkennung, infrastruktur-karte, staat-planung, dach-besonderheiten, ernaehrungs-biochemie, typische-fehler, budget-krisenvorsorge, szenarien
- **ng-anhang:** quellen, shops
- **Top-Level:** cover, inhalt, changelog, checklist, krisenkalender, einstieg-accordion, was-fehlt, szenariopfade

## Kritische Funktionen (duerfen nicht fehlen)
navTo, navSearch, buildSearchIndex, openTool, printSection, doPrint,
szpShow, szpBannerUpdate, szpBannerNav, szpBannerClose, szpReset, szpSave, szpLoad,
wfmRender, wfmInit, wfmSave, wfmToggle, wfmReset,
kkInit, kkRenderNav, kkRenderMonth, kkSave,
toggleSidebar, _injectChapterNav, _updateReadingUx, _markSectionRead, _initReadMarkers,
toggleBookmark, _injectBookmarkButtons, _refreshBookmarkUI, favClick,
_setupExternalLinks, toggleFontSize, _initFontSize, toggleGroup, _initNavGroupAria,
accToggle, _updateActiveNav, _updateReadProgress,
kpgAnswer, kpgShowResult, kpgReset, openGroupForSection, updateOnlineStatus

## Nav-Tracking (stabil seit V33.8)
- Algorithmus: "größter sichtbarer Flächenanteil im oberen 2/3 des Viewports"
- Öffnet Gruppe beim Scrollen (kein Reflow weil Sidebar position:fixed)
- Sidebar-Scroll via getBoundingClientRect (kein offsetTop)
- _updateReadingUx: Read-Tracking bei 80% gesehen
- _updateReadProgress: Fortschrittsanzeige, aufgerufen von _markSectionRead

## Features (V34.3)
- Fortschrittsanzeige Sidebar ("X von 87 Kapiteln gelesen")
- Krisenplan-Generator (8 Fragen, 3 Prioritätsstufen), dritter Accordion-Tab
- DACH-Besonderheiten Kapitel (DE/AT/CH)
- Fremde an der Tür -- in soziales-netzwerk
- PTSD & Trauma-Nachsorge -- in mental-staerke
- Intro-Text Cover: "Dieses Handbuch existiert weil..."
- Chapter-Nav Mobile Fix (flex-wrap, clamp)

## Design (nicht aendern)
- Mono-Font, Amber auf Dunkel, Militaer-Aesthetik -- Absicht
- Sidebar bleibt dunkel auch im Light-Mode (Light-Mode-Repair zerschoss Sidebar V33.1)
- Rhetorische Kurzsätze sind Stilmittel

## Preise (recherchiert Mai 2026, naechste Pruefung Nov 2026)
- Silber 1 oz: 90-110 EUR | Gold 1 oz: 2.900-3.200 EUR
- Sawyer Mini: 35-55 EUR | Sawyer Squeeze: 45-70 EUR
- GRAYL Ultrapress: 85-110 EUR | Leatherman Signal: 120-160 EUR
- Morakniv Garberg: 75-105 EUR | Olight Perun 2 Mini: 55-80 EUR
- Exped Versa 5R: 90-135 EUR | Snugpack Ionosphere: 100-200 EUR
- EcoFlow River 2 Max (512Wh): 300-400 EUR | Powerbank 20k mAh: 30-60 EUR
- Carinthia Defence 4: 180-250 EUR | DD Tarp 3x3: ca. 70 EUR

## Bekannte Bug-Geschichte
- V32.7: kpgShowResult einfache Quotes in HTML-Strings
- V32.8-V32.9: Hoisting-Fehler, progress-wrap vor html-Tag
- V33.3-V33.8: Mehrere orphaned JS-Blöcke
- V33.8 KRITISCH: Haupt-JS-Block beim Umordnen verloren -- aus V30.4 wiederhergestellt
- V33.9: Feuerdreieck SVG, Meta-Tag >>, l3-werkzeug-anchor
- Root Cause Nav-Sprung: HTML-Reihenfolge != Sidebar-Reihenfolge

## Offene Punkte
1. Linkrot-Check lokal: `python3 linkrot_check.py index.html`
2. Druck-Test: PDF aus Chrome
3. Preise: Naechste Pruefung Nov 2026

## Netzwerk
Container: nur api.anthropic.com, github.com, pypi.org etc. erlaubt.
Externe Seiten und linkrot_check.py nur lokal.
