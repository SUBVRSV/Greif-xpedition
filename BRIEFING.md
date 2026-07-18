# GREIF XPEDITION Krisenhandbuch -- Briefing für neuen Chat

## Projekt
Deutsches Krisenvorsorge-Handbuch von @greif_xpedition.
Single-HTML PWA. Gehostet: https://subvrsv.github.io/Greif-xpedition/ und https://greif-xpedition.subvrsv.de

## Aktueller Stand
**Version: V44.0** (Juli 2026)
93 Kapitel | ~1,79 MB | **6 JS-Blöcke** | ~131.000 Wörter
Alle Tests grün. Sidebar: **11 Gruppen** (ng-l3c und ng-zusatz wurden in V43.6 gesplittet).

## Dateien
- `index.html` -- alles inline (HTML + CSS + JS + base64-Bilder)
- `sw.js` -- Service Worker (Cache-Name: greif-V44.0 -- synchron mit HTML)
- `acceptance_test.py` / `test_nav.py` -- Testreihe (Achtung: nach Sandbox-Reset liegt in /mnt/user-data/uploads die ALTE Version mit Tests für entfernte Features krisenkalender/szpShow/kkInit -- diese Referenzen vor dem Lauf entfernen)
- `release_check.py` -- erwartet jetzt **6** JS-Blöcke (nicht 7)
- `linkrot_check.py` -- Linkrot-Checker, lokal beim User laufen lassen (Sandbox erreicht die meisten Domains nicht)
- `preview.png` -- 1200x630 OG-Bild, bei Kapitelzahl- oder Versionsänderung regenerieren (PIL-Skript, "93 Kapitel · V44.0")

## Core-Regeln
- Keine Em-Dashes (U+2014), nur `--`; korrekte Umlaute; keine Apostrophe in JS-Kommentaren
- Version +0.1 bei jeder Änderung in 4 HTML-Stellen (HTML-Kommentar, Sidebar-Footer, Cover-Meta, Cover-Notice) + sw.js Cache-Name
- `node --check` auf alle **6** JS-Blöcke nach jeder JS-Änderung
- `python3 release_check.py index.html VNEU VALT` muss "Alle Checks bestanden" liefern
- Immer BEIDE Dateien ausliefern: index.html + sw.js (plus preview.png, BRIEFING.md, release_check.py, linkrot_check.py via present_files)
- `navTo(id, link)` verwenden -- `navigateTo()` existiert NICHT
- Zwei Maps SYNCHRON halten: `const map` + `_navGroupMap` (beide in Haupt-JS-Block, je 2 Vorkommen)
- HTML-Reihenfolge der Sections = Sidebar-Reihenfolge (sonst Nav-Sprung beim Scrollen)

## In V43.x ENTFERNTE Features (nicht wieder einbauen, Reste nicht "reparieren")
Sofort-Panel, Schnellentscheider (qd*), Krisenplan-Generator (kpg*), Szenariopfade (szp*), Krisenkalender (kk*, war eigene Section), Wochennudge, Chapter-Completion-Toast, Keyboard-Shortcut-Popup, Persona-Karten. Der schwebende Notfall-Button (#emergency-btn) führt jetzt per openTool('notfall-triage') zur statischen Notfall-Übersicht im Cover.

## Verbliebene interaktive Features
Suche mit Highlight, Bookmarks/Favoriten (favorites-group), Resume-Banner (greif_lastRead), Fortschrittsring, Dark/Light-Mode (toggleTheme, Button: #light-mode-btn), PWA-Install, Vorratsplaner (vpCalc), Was-fehlt-mir (wfmInit), Notfall-Übersicht + Erste-10-Minuten + FAQ (Accordions, openTool mit toolIds), Familiennotfallplan-Inputs (fnpInit speichert per input-Listener in localStorage greif_fnp; Buttons als window.fnpPrint/fnpDownload/fnpExport/fnpReset), Kapitel-Link-Kopieren, Aktions-Box je Kapitel-Banner.

## Sidebar-Gruppen (11, seit V43.6)
- **ng-l1:** bug-out-bag, chest-pack, kleidung-ausruestung, tools-hacks, fluessigkeiten-bob
- **ng-l1b:** nahrung-konzept, essensplan, einkaufsliste, nahrung-lagerung, feldkueche, nahrung-naehrstoffe
- **ng-l2:** medizin-erstehilfe, medikamente-vorrat, medizin-ohne-arzt, hygiene-sanitaer, haushalts-ressourcen, kommunikation-krise, navigation-krise, energie-strom, technik-field, finanzen-dokumente, finanzkrise, digitale-vorbereitung, soziales-netzwerk
- **ng-l3a (Wohnen & Sicherheit):** werkzeug-zuhause, wasservorrat, fahrzeug-krise, mobilitaet-krise, shelter-evakuierung, **extremwetter-unterwegs (NEU V43.7)**, urban-wohnen, urban-mietwohnung, wohnung-absichern, sicherheit-lager, selbstverteidigung, freie-waffen
- **ng-l3b (Wildnis & Versorgung):** wildnis-bushcraft, tiere-fruehwarnung, tarp-aufbau, feuer-bedingungen, signalisierung, anbau-konservierung, langzeitlager, jagd-nahrung, heizung-waerme, saisonale-anpassung
- **ng-l3c1 (Infrastruktur-Krisen):** blackout-matrix, blackout-stufenplan, gasausfall-szenario, solarsturm-szenario, lieferketten-ausfall, cyberangriff, drohnen-schutz
- **ng-l3c2 (Katastrophen, Personen & Recht):** naturgefahren, hitzewelle, abc-schutz, epidemiologie-krise, pandemie-biobedrohung, krieg-unruhen, familiennotfallplan, alleinstehende-krise, behinderung-krise, haustier-krise (NEU V42.9), recovery-nachkrise (NEU V42.9), recht-krisenfall
- **ng-alltag:** sanitaer-notfall, brand-notfall, gasaustritt, krisenkueche, ausruestungspflege, bartering, kinder-krise
- **ng-zusatz1 (Körper, Geist & Werkstatt):** mental-staerke, koerperliche-fitness, schlaf-krise, ernaehrungs-biochemie, reparieren-krise, offline-bibliothek
- **ng-zusatz2 (Recht, System & Kontext):** budget-krisenvorsorge, dach-besonderheiten, mietrecht-krise, staat-planung, desinformation-krise, gefahrenerkennung, warnmeldungen, infrastruktur-karte, szenarien, typische-fehler
- **ng-anhang:** quellen, shops
- **Top-Level ohne Gruppe:** cover, inhalt, checklist

## JS-Blöcke (6, seit V43.1)
- Block 0/1: Theme-Init (je ~140 B)
- Block 2: Vorratsplaner-Daten (~8 KB)
- Block 3: Haupt-JS (~68 KB) -- navTo, const map, _navGroupMap, Suche, Bookmarks, openTool, fnpInit
- Block 4: PWA SW-Registration (~2 KB)
- Block 5: Online-Status, Fortschrittsring, FNP-Buttons als window.* (~10 KB)

## Faktencheck-Historie (Stufen 1-4 plus Medizin, alle abgeschlossen)
- **V42.1:** Warntag = ZWEITER Do im Sept; Cell Broadcast Test 8.12.2022 / Wirkbetrieb 23.2.2023; TAB-Bericht 2011 (Petermann et al., nicht "Bundestag-Bericht"); BfArM führt Engpassliste (nicht ABDA, 892 Meldungen 2024); KIRAS-Studie EV-A 2015 (nicht "Saurugg 2021")
- **V42.2:** Balkonkraftwerk seit 16.5.2024: 800W WR / 2000Wp Module, Anmeldung NUR MaStR (Netzbetreiber-Anmeldung entfallen); Kleinwindanlage 50-800 kWh/JAHR (nicht Monat); EcoFlow River 2 Pro 768Wh/800W, Max 512Wh (kein "Trail" in der Serie)
- **V42.3:** Sicherheitspaket 31.10.2024: §42b WaffG (Messerverbot Fernverkehr/Bahnhöfe, BW auch ÖPNV seit 22.7.2025), §42c (anlasslose Kontrollen), §42 neu (Veranstaltungen); Tonfa/Teleskopschlagstock LEGAL zu besitzen (nur Führverbot §42a); Springmesser seit 31.10.2024 verboten; Tierabwehrspray OHNE gesetzliche Altersgrenze
- **V42.4:** §138 AO = Auslandsbeteiligungen (Konten laufen über CRS); AWV-Grenze 50.000 EUR seit 1.1.2025 (war im Handbuch schon korrekt); Einlagensicherung 100k/7 Arbeitstage ist gesetzlich und wird eingehalten (Greensill 2021); Verteidigungsfall = Art. 115a GG
- **V42.5/V42.6:** ESEE 4: 160-190 EUR; Olight Perun 2 Mini: 70-110 EUR; Leatherman Signal: 125-165 EUR; Gold/Silber nur noch mit Datumsstand + Volatilitätshinweis; Amateurfunk Klasse E: 4 KW-Bänder (160/80/15/10m), Klasse N seit 24.6.2024
- **V44.0 (Medizin):** Jodblockade SSK: 13-45 Jahre 130mg (nicht 13-17), über 45 ABRATUNG, Schwangere 130mg altersunabhängig, Kinderdosen 16,25/32,5/65mg; Ibuprofen Selbstmedikation max 1,2g/Tag (2,4g nur ärztlich); H2O2 ist KEINE Trinkwasser-Desinfektion; kolloidales Silber: BfR rät ab (nur Silberionen-Konservierung für sauberes Wasser); "chlorfreies Natriumhypochlorit" war Unsinn → "unparfümiert"

## Preise (Stand Juli 2026, nächste Prüfung Jan 2027)
Silber 1oz: ~75-85 EUR (volatil! Spot 2026: 55-120 USD) | Gold 1oz: 3.100-3.500 EUR | Sawyer Mini: 35-55 | GRAYL Ultrapress: 85-110 | Morakniv Garberg: 75-105 | Leatherman Signal: 125-165 | ESEE 4: 160-190 | EcoFlow River 2 Max: 300-400 | Carinthia Defence 4: 180-250 | Olight Perun 2 Mini: 70-110

## Feedback-Kanal (seit V43.0)
Im Quellen-Kapitel + beiden Preishinweisen: @greif_xpedition (Twitter/X), github.com/subvrsv/Greif-xpedition (Repo existiert, public, verifiziert), greif-xpedition.subvrsv.de. Changelog-Tabelle im Quellen-Kapitel pflegen!

## NICHT ANFASSEN
Cover-Struktur, Light-Mode CSS (Sidebar bleibt dunkel), Nav-Algorithmus (stabil seit V36.5), Akkordeon-Handler (document-Listener auf [data-acc]), Sidebar-Scrollbar (versteckt), dünne Kapitel (bewusst kompakt), mental-staerke + budget-krisenvorsorge Ton (passt).

## Offene Punkte / bewusst nicht gemacht
- ~500 Rest-Preise, Zeitangaben, Gewichte ungeprüft (geringes Risiko, Feedback-Kanal + Jan-2027-Prüfung)
- Dateigröße-Optimierung verworfen (nur 90 KB Bilder, Rest Text; gzip macht der Server)
- Kapitel-individuelle Änderungsdaten verworfen (Changelog-Tabelle löst das)
- linkrot_check.py sollte der User lokal laufen lassen (100 externe URLs, v.a. Amazon-Links altern schnell)
