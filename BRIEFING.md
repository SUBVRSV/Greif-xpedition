# GREIF XPEDITION Krisenhandbuch -- Briefing für neuen Chat

## Projekt
Deutsches Krisenvorsorge-Handbuch von @greif_xpedition.
Single-HTML PWA. Gehostet: https://subvrsv.github.io/Greif-xpedition/ und https://greif-xpedition.subvrsv.de

## Aktueller Stand
**Version: V44.3** (Juli 2026)
94 Kapitel | ~1,79 MB | **6 JS-Blöcke** | ~131.000 Wörter
Alle Tests grün. Sidebar: **11 Gruppen** (ng-l3c und ng-zusatz wurden in V43.6 gesplittet).

## Dateien
- `index.html` -- alles inline (HTML + CSS + JS + base64-Bilder)
- `sw.js` -- Service Worker (Cache-Name: greif-V44.3 -- synchron mit HTML)
- `acceptance_test.py` / `test_nav.py` -- Testreihe (Achtung: nach Sandbox-Reset liegt in /mnt/user-data/uploads die ALTE Version mit Tests für entfernte Features krisenkalender/szpShow/kkInit -- diese Referenzen vor dem Lauf entfernen)
- `release_check.py` -- erwartet jetzt **6** JS-Blöcke (nicht 7)
- `linkrot_check.py` -- Linkrot-Checker, lokal beim User laufen lassen (Sandbox erreicht die meisten Domains nicht)
- `preview.png` -- 1200x630 OG-Bild, bei Kapitelzahl- oder Versionsänderung regenerieren (PIL-Skript, "94 Kapitel · V44.3")

## Core-Regeln
- Keine Em-Dashes (U+2014), nur `--`; korrekte Umlaute; keine Apostrophe in JS-Kommentaren
- ACHTUNG sed-Falle: globales sed 's/VALT/VNEU/g' zieht auch die oberste Zeile der Changelog-Tabelle im Quellen-Kapitel hoch und zerstört die Historie. Nach jedem Versions-Bump die Changelog-Tabelle prüfen! Besser: Changelog-Eintrag NACH dem sed einfügen.
- Version +0.1 bei jeder Änderung in 4 HTML-Stellen (HTML-Kommentar, Sidebar-Footer, Cover-Meta, Cover-Notice) + sw.js Cache-Name
- `node --check` auf alle **6** JS-Blöcke nach jeder JS-Änderung
- `python3 release_check.py index.html VNEU VALT` muss "Alle Checks bestanden" liefern
- Immer BEIDE Dateien ausliefern: index.html + sw.js (plus preview.png, BRIEFING.md, release_check.py, linkrot_check.py via present_files)
- `navTo(id, link)` verwenden -- `navigateTo()` existiert NICHT
- Zwei Maps SYNCHRON halten: `const map` + `_navGroupMap` (beide in Haupt-JS-Block, je 2 Vorkommen)
- HTML-Reihenfolge der Sections = Sidebar-Reihenfolge (sonst Nav-Sprung beim Scrollen)
- Neue Kapitel an DREI Stellen eintragen: Section-HTML, Sidebar-Link, Inhaltsverzeichnis (section id=inhalt) -- das TOC wurde von V41.5 bis V44.1 vergessen

## In V43.x ENTFERNTE Features (nicht wieder einbauen, Reste nicht "reparieren")
Sofort-Panel, Schnellentscheider (qd*), Krisenplan-Generator (kpg*), Szenariopfade (szp*), Krisenkalender (kk*, war eigene Section), Wochennudge, Chapter-Completion-Toast, Keyboard-Shortcut-Popup, Persona-Karten. Der schwebende Notfall-Button (#emergency-btn) führt jetzt per openTool('notfall-triage') zur statischen Notfall-Übersicht im Cover.

## Verbliebene interaktive Features
Suche mit Highlight, Bookmarks/Favoriten (favorites-group), Resume-Banner (greif_lastRead), Fortschrittsring, Dark/Light-Mode (toggleTheme, Button: #light-mode-btn), Schriftgrößen-Regler A/A+/A++ (toggleFontSize, #fontsize-toggle, body.fz-large/.fz-xlarge via zoom), PWA-Install, Vorratsplaner (vpCalc), Was-fehlt-mir (wfmInit), Notfall-Übersicht + Erste-10-Minuten + FAQ (Accordions, openTool mit toolIds), Familiennotfallplan-Inputs (fnpInit speichert per input-Listener in localStorage greif_fnp; Buttons als window.fnpPrint/fnpDownload/fnpExport/fnpReset), Kapitel-Link-Kopieren, Aktions-Box je Kapitel-Banner.

## Sidebar-Gruppen (11, seit V43.6)
- **ng-l1:** bug-out-bag, chest-pack, kleidung-ausruestung, tools-hacks, fluessigkeiten-bob
- **ng-l1b:** nahrung-konzept, essensplan, einkaufsliste, nahrung-lagerung, feldkueche, nahrung-naehrstoffe
- **ng-l2:** medizin-erstehilfe, medikamente-vorrat, medizin-ohne-arzt, hygiene-sanitaer, haushalts-ressourcen, kommunikation-krise, navigation-krise, energie-strom, technik-field, finanzen-dokumente, finanzkrise, digitale-vorbereitung, soziales-netzwerk
- **ng-l3a (Wohnen & Sicherheit):** werkzeug-zuhause, wasservorrat, fahrzeug-krise, mobilitaet-krise, shelter-evakuierung, **extremwetter-unterwegs (NEU V43.7)**, urban-wohnen, urban-mietwohnung, wohnung-absichern, sicherheit-lager, selbstverteidigung, freie-waffen
- **ng-l3b (Wildnis & Versorgung):** wildnis-bushcraft, tiere-fruehwarnung, tarp-aufbau, feuer-bedingungen, signalisierung, anbau-konservierung, langzeitlager, jagd-nahrung, heizung-waerme, saisonale-anpassung
- **ng-l3c1 (Infrastruktur-Krisen):** blackout-matrix, blackout-stufenplan, gasausfall-szenario, solarsturm-szenario, lieferketten-ausfall, cyberangriff, drohnen-schutz
- **ng-l3c2 (Katastrophen, Personen & Recht):** naturgefahren, hitzewelle, abc-schutz, epidemiologie-krise, pandemie-biobedrohung, krieg-unruhen, familiennotfallplan, alleinstehende-krise, behinderung-krise, senioren-krise (NEU V44.3), haustier-krise (NEU V42.9), recovery-nachkrise (NEU V42.9), recht-krisenfall
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
- **V44.3 (Medizin):** Jodblockade SSK: 13-45 Jahre 130mg (nicht 13-17), über 45 ABRATUNG, Schwangere 130mg altersunabhängig, Kinderdosen 16,25/32,5/65mg; Ibuprofen Selbstmedikation max 1,2g/Tag (2,4g nur ärztlich); H2O2 ist KEINE Trinkwasser-Desinfektion; kolloidales Silber: BfR rät ab (nur Silberionen-Konservierung für sauberes Wasser); "chlorfreies Natriumhypochlorit" war Unsinn → "unparfümiert"

## Preise (Stand Juli 2026, nächste Prüfung Jan 2027)
Silber 1oz: ~75-85 EUR (volatil! Spot 2026: 55-120 USD) | Gold 1oz: 3.100-3.500 EUR | Sawyer Mini: 35-55 | GRAYL Ultrapress: 85-110 | Morakniv Garberg: 75-105 | Leatherman Signal: 125-165 | ESEE 4: 160-190 | EcoFlow River 2 Max: 300-400 | Carinthia Defence 4: 180-250 | Olight Perun 2 Mini: 70-110

## Feedback-Kanal (seit V43.0)
Im Quellen-Kapitel + beiden Preishinweisen: @greif_xpedition (Twitter/X), github.com/subvrsv/Greif-xpedition (Repo existiert, public, verifiziert), greif-xpedition.subvrsv.de. Changelog-Tabelle im Quellen-Kapitel pflegen!

## NICHT ANFASSEN
Cover-Struktur, Light-Mode CSS (Sidebar bleibt dunkel), Nav-Algorithmus (stabil seit V36.5), Akkordeon-Handler (document-Listener auf [data-acc]), Sidebar-Scrollbar (versteckt), dünne Kapitel (bewusst kompakt), mental-staerke + budget-krisenvorsorge Ton (passt).



## BUCH-PROJEKT (NEU, seit V44.3)
Zweite Datei **buch.html** = erzählendes Begleitbuch "Wenn es ernst wird". Eigenständiger Sachbuch-Text (geschichten-getrieben, Szene-Einstieg), verlinkt punktuell ins Handbuch (index.html#kapitel). Umgekehrt: Buch-Banner im Handbuch-Cover verlinkt auf buch.html.
- Eigene Optik: Serifenschrift (Spectral via Google Fonts), Papier-hell als Default, Dark-Mode optional, Buchspalte (--measure 34rem), Drop-Cap, Pull-Quotes, Szene-Blöcke, Fußnoten. Teilt Amber-Akzent mit Handbuch.
- Offline: buch.html ist in sw.js URLS aufgenommen (greif-V44.3 Cache).
- Struktur skalierbar: Kapitel als <article class="chapter" id="kap-N">. BUCH KOMPLETT + VOLL VERTIEFT (V3.0): alle 10 Kapitel auf je ~1550-1900 Wörter, gesamt ~16.900 Wörter / ~67 Buchseiten. Jedes Kapitel hat 2. Fallbeispiel + Belege + Verzahnung. Vertiefungs-Fallbeispiele: K1 Ahrtal-Chronologie, K2 Texas/Uri, K3 Sipplingen+Notbrunnen, K4 Iberien 2025, K5 Hamster-Psychologie/JIT, K6 CO-Gefahr, K7 Warnmittel-Mix, K8 Ahrtal-Helferwelle, K9 OPLAN DEU/dt. Zivilschutz, K10 Schluss-Bogen. Kälte-Passage K6 korrigiert (nicht wieder aufweichen). Alle Em-dash-frei, alle Handbuch-Links valide. plus Inhaltsübersicht mit ganzer Dramaturgie. Kapitel 1 "Die zwei Wochen, in denen alles anders war" (~1080 Wörter, Ahrtal-2021-Einstieg). Kapitel 2 nur Platzhalter.
- Ton (vom User festgelegt): geschichten-getrieben, echte Fälle als Szene-Einstieg, dann Erklärung. NICHT belehrend, NICHT Weltuntergang. Kein langweiliges Sachbuch.
- Buch-Kapitel spiegeln grob Handbuch-Themen, jedes zeigt via .to-handbook-Box auf mehrere Handbuch-Kapitel.
- Em-Dash-Regel gilt AUCH im Buch (Konsistenz, release_check-kompatibel).
- FESTGELEGTE DRAMATURGIE (10 Kapitel, im Buch als Inhaltsübersicht #toc sichtbar):
  Teil I Warum überhaupt: (1) Die zwei Wochen in denen alles anders war [FERTIG, Ahrtal], (2) Die 72 Stunden die über alles entscheiden [FERTIG, Italien-Blackout 2003-Einstieg, ~1170 Wörter]
  Teil II Grundbedürfnisse: (3) Wasser [FERTIG, Utrecht-2015-Einstieg, ~1075 Wörter], (4) Wenn das Licht ausgeht [FERTIG, Nordamerika-2003-Einstieg/Kaskade, ~1076 Wörter], (5) Vorrat oder die Kunst satt zu bleiben [FERTIG, Klopapier-2020-Einstieg/lebender Vorrat, ~990 Wörter], (6) Wärme Licht und ein Dach [FERTIG, ~1160 Wörter; Kälte-Passage in V1.10 präzisiert: 13-16 Grad nur bei bewegungslos+dünn+Risikofaktor, gesunder Erwachsener nicht gefährdet]
  Teil III Schwierigere Wahrheiten: (7) Wenn die Netze schweigen [FERTIG, Kein-Netz-trotz-Akku-Einstieg, ~1110 Wörter, START Teil III], (8) Die anderen [FERTIG, Desaster-Mythen/Solidarität-Einstieg, ~1126 Wörter, Wendepunkt Ich→Wir], (9) Das Undenkbare denken [FERTIG, Schweden-Broschüre-Einstieg, ~1053 Wörter, entpolitisiert], (10) Danach [FERTIG, Ahrtal-Rückkehr-Einstieg, ~1180 Wörter, versöhnlicher Schluss]
  Prinzip: Risiken werden nach hinten größer/unbequemer, parallel wächst Leser-Zutrauen. Krieg NIE am Anfang. Je Kapitel ~1000-2000 Wörter. Buch überzeugt+verweist, Detail liegt im Handbuch.
  ACHTUNG: Kap 1 nutzt Ahrtal schon als Warum-Aufhänger. Ein späteres Hochwasser-Detail müsste anderen Winkel haben (Sturzflut-Mechanik, Vorwarnzeit).
- Eigene Versionierung: buch.html hat V3.0 im HTML-Kommentar (unabhängig von Handbuch-Version).



## AGENTEN-PROJEKT (NEU, Stufe 1 fertig)
Ziel: weitergebbarer Krisenvorsorge-Assistent aus Handbuch+Buch. Konzept 3-stufig, kostenlos+unabhängig (User-Wunsch): (1) Einspiel-Paket [FERTIG], (2) Offline-Assistenten-Seite [FERTIG: assistent.html], (3) dieselbe Seite optional mit echter KI per User-eigenem API-Key [GEPLANT].
Fundament = Wissensbasis, einmal gebaut, speist alle Stufen:
- wissensbasis.json (1,1 MB, Volltext aller 94 HB-Sections + 10 Buch-Kapitel, strukturiert {handbuch:[{id,title,subtitle,text}], buch:[...]})
- wissensbasis-kompakt.md (126 KB, ~17k Wörter, Kernaussagen+Bullets pro Kapitel, mit Kapitel-IDs für Verweise, passt in KI-Umgebungen)
- systemprompt.md (Verhaltensanweisung: nur aus Material antworten, Quellkapitel nennen, Ton ruhig/sachlich, Sicherheitsregeln 112/CO/Recht, Stand Juli 2026)
- ANLEITUNG.md (4 Varianten: ChatGPT-GPT, Claude-Projekt, einmaliges Gespräch, lokale KI)
Alle em-dash-frei. PLUS uebersicht.html (Projekt-Schaubild V1.0, 10 KB: 3 Ebenen Inhalt→Wissensbasis→3 Stufen, Dateientabelle, Wegplan; Ampel grün/amber/grau; V1.1 mit Zukunftsvision-Sektion: Methode übertragbar auf andere Krisen (Trennung/Jobverlust/Krankheit/Tod), getrennte Projekte + gemeinsames Dach, ROTE Leitplanke: bei Leid-Themen nur Erst-Wegweiser + Weiterleitung zu Fachleuten, nie Beratung; GREIF hat Prio, Rest später). PLUS pitch.html (Pitch-Infografik V1.0, 6 KB: Hero + USP-Band 'jede Angabe geprüft' + Statt/Bei-uns-Kontrast + 4 Säulen geprüft/keine-Halluzination/Praxis/Mensch + Kennzahlen 94/10/1/∞; für Präsentationen, visuell geprüft). STUFE 2 FERTIG: assistent.html V1.1 (934 KB, offline, single-file). Frage-orientierte Suche (searchdata.json eingebettet, 104 Einträge mit kw/tkw/points), Synonym-Erweiterung + ID-Match + Titel-Gewichtung, Antwort=beste Karte + weitere relevante, Kernpunkte + Kapitel-Link (amber=Handbuch, blau=Buch), Sicherheitshinweis bei Notfall-Keywords→112. Nav-Rest aus 70 Kapiteln bereinigt. In sw.js-Cache. Handbuch-Cover + Buch-Topbar verlinken jetzt auf assistent.html. Visuell + mehrfach-Suche getestet (6/6 verschieden), JS ok, em-dash-frei. V1.1-Fix: zentrale go()-Funktion statt Inline-Handler, scrollIntoView ersetzt durch sanftes window.scrollTo (Bug "Suche geht nur 1x" behoben, Ursache war vmtl. SW-Cache + Auto-Scroll); sw.js Cache-Version hochgezogen.
PLUS Such-Brücke: Handbuch-navSearch zeigt bei fragen-artiger Eingabe (>=3 Wörter oder ?) einen Berater-Hinweis mit Link assistent.html?q=<frage>; assistent.html V1.2 liest ?q= aus URLSearchParams und sucht automatisch. Beide Suchen bleiben schlank, keine Datendopplung. Getestet. NÄCHSTES: Stufe 3 = KI-Schalter in assistent.html (optionaler eigener API-Key → frei formulierender Assistent auf gleicher Wissensbasis).

## Offene Punkte / bewusst nicht gemacht
- ~500 Rest-Preise, Zeitangaben, Gewichte ungeprüft (geringes Risiko, Feedback-Kanal + Jan-2027-Prüfung)
- Dateigröße-Optimierung verworfen (nur 90 KB Bilder, Rest Text; gzip macht der Server)
- Kapitel-individuelle Änderungsdaten verworfen (Changelog-Tabelle löst das)
- linkrot_check.py sollte der User lokal laufen lassen (100 externe URLs, v.a. Amazon-Links altern schnell)
