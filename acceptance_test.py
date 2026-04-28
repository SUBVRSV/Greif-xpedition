#!/usr/bin/env python3
"""
Akzeptanz-Test fuer GREIF XPEDITION Krisenhandbuch.
Prueft ob alle UX-Komponenten und JS-Funktionen vorhanden sind.

Aufruf: python3 acceptance_test.py [pfad/zu/index.html]
Exit 0 = alle Tests bestanden, Exit 1 = mindestens ein Test fehlgeschlagen
"""
import re
import sys
from bs4 import BeautifulSoup


def run_tests(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    soup = BeautifulSoup(content, 'html.parser')

    results = []
    failed = []

    def test(name, condition, detail=''):
        if condition:
            results.append(('OK', name, detail))
        else:
            results.append(('FAIL', name, detail))
            failed.append(name)

    # === STRUKTUR ===
    sections = soup.find_all('section', id=True)
    test('Mindestens 80 Kapitel', len(sections) >= 80, f'gefunden: {len(sections)}')
    test('Section-Balance', content.count('<section id="') == content.count('</section>'),
         f'open: {content.count("<section id=")}, close: {content.count("</section>")}')

    # Wichtige Kapitel
    required_sections = [
        'cover', 'bug-out-bag', 'kleidung-ausruestung', 'medizin-erstehilfe',
        'wasservorrat', 'energie-strom', 'familiennotfallplan',
        'hitzewelle', 'naturgefahren', 'pandemie-biobedrohung',
        'kinder-krise', 'krisenkalender', 'checklist',
    ]
    for sid in required_sections:
        test(f'Section "{sid}" existiert', soup.find('section', id=sid) is not None)

    # === COPYRIGHT/CONTENT ===
    test('Keine Em-Dashes', content.count('\u2014') == 0,
         f'{content.count(chr(0x2014))} gefunden')

    # === MOBILE-UX (V27.1) ===
    test('Mobile-Topbar HTML vorhanden', 'id="mobile-topbar"' in content)
    test('Mobile-Topbar CSS vorhanden', '#mobile-topbar {' in content)
    test('Burger 40x40px', 'width: 40px; height: 40px;' in content)

    # === READING UX (V27.2 / V29.0) ===
    # Reading-Progress, Mini-Header, Resume-Banner wurden in V29.0 entfernt
    test('_injectChapterNav fn', 'function _injectChapterNav' in content)
    test('Body max-width 72ch', 'max-width: 72ch;' in content)

    # === FARBSCHEMA (V27.4) ===
    colors = set(re.findall(r'border-left-color:\s*(#[0-9a-fA-F]+)', content))
    banner_colors = set()
    for s in sections:
        banner = s.find('div', class_='section-banner')
        if banner:
            style = banner.get('style', '')
            m = re.search(r'border-left-color:\s*(#[0-9a-fA-F]+)', style)
            if m:
                banner_colors.add(m.group(1))
    test('Banner-Farbschema reduziert', len(banner_colors) <= 12,
         f'{len(banner_colors)} unique')

    # === BOOKMARKS (V27.6, V28.3) ===
    test('Bookmark CSS', '.bookmark-btn {' in content)
    test('Favoriten-Gruppe HTML', 'id="favorites-group"' in content)
    test('toggleBookmark fn', 'function toggleBookmark' in content)
    test('Bookmark active state',
         '.bookmark-btn.active {' in content and 'background: var(--amber)' in content)

    # === FAVORITEN-FIX (V28.4) ===
    test('favClick fn (Mobile-Auto-Close)', 'function favClick' in content)
    test('data-fav-id Attribut', 'data-fav-id' in content)

    # === EXTERNAL LINKS (V27.7) ===
    test('External Links CSS',
         'a[href^="http"]:not([href*="greif-xpedition"])' in content)
    test('External Links JS', '_setupExternalLinks' in content)

    # === RESUME BANNER === entfernt in V29.0

    # === PERSONA (V27.9) ===
    test('Persona-CSS', '.persona-card {' in content)
    test('Persona-Karten HTML', 'id="persona-start"' in content)

    # === PRINT (V28.0) ===
    test('Print-CSS Mobile-Topbar hidden', '@media print' in content and '#mobile-topbar' in content)
    test('Print Tabellen-Pagination', 'page-break-inside: avoid' in content)

    # === KEYBOARD SHORTCUT (V28.7+) ===
    test('Keyboard-Shortcut /', 'e.key === \'/\'' in content)

    # === TABELLEN-FIX (V28.7) ===
    # Inkonsistente Spalten
    inconsistent_count = 0
    for t in soup.find_all('table'):
        rows = t.find_all('tr')
        cell_counts = []
        for r in rows:
            cells = r.find_all(['th', 'td'])
            colspan_total = sum(int(c.get('colspan', 1)) for c in cells)
            cell_counts.append(colspan_total)
        if cell_counts and len(set(cell_counts)) > 1:
            inconsistent_count += 1
    test('Tabellen-Konsistenz', inconsistent_count == 0,
         f'{inconsistent_count} inkonsistent')

    # === LIGHT MODE (Briefing-Anforderung) ===
    test('Light-Mode Default',
         '<body class="light-mode">' in content)

    # === KRITISCHE JS-FUNKTIONEN ===
    critical_fns = [
        '_updateActiveNav', '_allSections', '_navGroupMap',
        'navSearch', 'navTo', 'buildSearchIndex', 'szpShow',
        'szpBannerUpdate', 'wfmRender', 'kkInit',
        'toggleSidebar',
    ]
    for fn in critical_fns:
        test(f'JS: {fn}', fn in content)

    # === REPORT ===
    print(f'\n{"=" * 60}')
    print(f'AKZEPTANZ-TEST: {filepath}')
    print(f'{"=" * 60}\n')
    for status, name, detail in results:
        prefix = '\u2713' if status == 'OK' else '\u2717'
        print(f'  {prefix} {name}' + (f'  ({detail})' if detail else ''))

    total = len(results)
    ok = total - len(failed)
    print(f'\n{"=" * 60}')
    print(f'{ok}/{total} Tests bestanden')
    if failed:
        print(f'\nFEHLGESCHLAGEN:')
        for f in failed:
            print(f'  - {f}')
    print(f'{"=" * 60}\n')
    return len(failed) == 0


if __name__ == '__main__':
    fp = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/index.html'
    success = run_tests(fp)
    sys.exit(0 if success else 1)
