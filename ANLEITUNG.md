# GREIF XPEDITION Krisenvorsorge-Assistent – Anleitung

So machst du aus dem GREIF-Wissen deinen eigenen KI-Berater. Drei Dateien gehören zusammen:

- **wissensbasis-kompakt.md** – das komprimierte Wissen (empfohlen, passt in fast jede KI-Umgebung)
- **wissensbasis.json** – der vollständige Volltext (für Umgebungen, die große Dateien verarbeiten)
- **systemprompt.md** – die Verhaltensanweisung für die KI

Du brauchst kein Programmierwissen. Wähle die Umgebung, die du nutzt:

## Variante 1: ChatGPT (eigener GPT)
1. Gehe zu "GPTs" → "Erstellen".
2. Füge unter "Anweisungen" den Text aus `systemprompt.md` ein (nur den Teil unterhalb der Trennlinie).
3. Lade unter "Wissen" die Datei `wissensbasis-kompakt.md` hoch.
4. Gib dem GPT einen Namen (z. B. "GREIF Krisenberater") und speichere. Fertig. Du kannst ihn privat nutzen oder per Link teilen.

## Variante 2: Claude (Projekt)
1. Erstelle ein neues "Projekt".
2. Füge den Text aus `systemprompt.md` als "Projektanweisungen" ein.
3. Lade `wissensbasis-kompakt.md` in das Projektwissen hoch.
4. Stelle deine Fragen im Projekt. Fertig.

## Variante 3: Beliebige KI (einmaliges Gespräch)
Wenn deine KI-Umgebung keine dauerhaften Projekte kennt, geht es auch so:
1. Beginne ein neues Gespräch.
2. Kopiere zuerst den Systemprompt hinein, dann den Inhalt von `wissensbasis-kompakt.md` (bei Längenbegrenzung in mehreren Teilen).
3. Danach kannst du frei fragen. Das Wissen gilt für dieses eine Gespräch.

## Variante 4: Lokale / offline KI
Wer eine lokale KI betreibt (z. B. über eine der gängigen Desktop-Anwendungen für Sprachmodelle), lädt `systemprompt.md` als System-Prompt und `wissensbasis-kompakt.md` als Wissensquelle. So läuft der Berater komplett offline auf dem eigenen Rechner.

---

**Wichtig:** Der Assistent ersetzt keine Rettungskräfte. Bei akuter Gefahr immer 112 wählen. Das Wissen hat den Stand Juli 2026; Preise, Gesetze und Technik können sich ändern. Aktuelles immer unter @greif_xpedition.
