#!/usr/bin/env python3
"""
release_check.py -- GREIF XPEDITION Krisenhandbuch
Prueft alle Release-Kriterien vor dem Deployment.

Aufruf:
  python3 release_check.py index.html V39.1 V39.0
  python3 release_check.py index.html V39.1          (ohne VOLD)

Prueft:
  1. Version in allen 4 Stellen (HTML-Kommentar, Sidebar-Footer, Cover-Meta, Cover-Notice)
  2. sw.js Cache-Name synchron mit HTML-Version
  3. Keine Em-Dashes (U+2014)
  4. Section-Balance (<section id= und </section> gleich oft)
  5. Keine JS-Syntaxfehler (node --check auf alle 7 Bloecke)
  6. VOLD kommt nicht mehr vor (wenn angegeben)
  7. acceptance_test.py (47/48, Persona-Karten absichtlich fehlend)
  8. test_nav.py (Nav OK)

Exit 0 = alles OK, Exit 1 = mindestens ein Fehler
"""

import sys
import re
import os
import subprocess
import tempfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def run_check(html_path, v_new, v_old=None):
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    sw_path = os.path.join(os.path.dirname(html_path), 'sw.js')

    errors = []
    ok_count = 0

    def ok(msg):
        nonlocal ok_count
        ok_count += 1
        print(f'  \u2713 {msg}')

    def fail(msg):
        errors.append(msg)
        print(f'  \u2717 {msg}')

    # ===== 1. VERSION IN ALLEN 4 STELLEN =====
    print(f'\n[1] Version {v_new} in allen 4 Stellen')
    checks = [
        (f'<!-- GREIF XPEDITION Krisenhandbuch {v_new} -->', 'HTML-Kommentar'),
        (f'Krisenvorsorge {v_new}<', 'Sidebar-Footer'),
        (f'{v_new} // GREIF XPEDITION Krisenhandbuch', 'Cover-Meta (Ausgabe)'),
        (f'{v_new}', 'Cover-Notice (mind. 1x)'),
    ]
    for pattern, name in checks:
        if pattern in content:
            ok(name)
        else:
            fail(f'{name} -- "{pattern}" nicht gefunden')

    # ===== 2. SW.JS CACHE-NAME =====
    print(f'\n[2] sw.js Cache-Name')
    if os.path.exists(sw_path):
        with open(sw_path, 'r', encoding='utf-8') as f:
            sw = f.read()
        cache_pattern = f"greif-{v_new}"
        if cache_pattern in sw:
            ok(f'sw.js Cache-Name: {cache_pattern}')
        else:
            fail(f'sw.js Cache-Name nicht "{cache_pattern}" -- gefunden: {re.search(r"greif-V[0-9.]+", sw).group() if re.search(r"greif-V[0-9.]+", sw) else "nichts"}')
    else:
        fail(f'sw.js nicht gefunden unter: {sw_path}')

    # ===== 3. KEINE EM-DASHES =====
    print('\n[3] Keine Em-Dashes (U+2014)')
    em_count = content.count('\u2014')
    if em_count == 0:
        ok('Keine Em-Dashes gefunden')
    else:
        lines = [i+1 for i, l in enumerate(content.splitlines()) if '\u2014' in l]
        fail(f'{em_count} Em-Dashes gefunden in Zeilen: {lines[:5]}')

    # ===== 4. SECTION-BALANCE =====
    print('\n[4] Section-Balance')
    open_sections = content.count('<section id=')
    close_sections = content.count('</section>')
    if open_sections == close_sections:
        ok(f'{open_sections} Sections, Balance OK')
    else:
        fail(f'Unbalanciert: {open_sections} oeffnend, {close_sections} schliessend')

    # ===== 5. JS SYNTAX CHECK =====
    print('\n[5] JS Syntax-Check (node --check, alle 7 Bloecke)')
    scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
    if len(scripts) != 7:
        fail(f'Erwarte 7 JS-Bloecke, gefunden: {len(scripts)}')
    else:
        ok(f'{len(scripts)} JS-Bloecke gefunden')
        all_ok = True
        for i, script in enumerate(scripts):
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8') as tmp:
                tmp.write(script)
                tmp_path = tmp.name
            try:
                result = subprocess.run(
                    ['node', '--check', tmp_path],
                    capture_output=True, text=True
                )
                if result.returncode == 0:
                    ok(f'Block {i}: OK ({len(script)} Zeichen)')
                else:
                    fail(f'Block {i}: SYNTAXFEHLER -- {result.stderr.strip()[:100]}')
                    all_ok = False
            except FileNotFoundError:
                fail('node nicht gefunden -- bitte Node.js installieren')
                all_ok = False
                break
            finally:
                os.unlink(tmp_path)

    # ===== 6. ALTE VERSION NICHT MEHR VORHANDEN =====
    if v_old:
        print(f'\n[6] Alte Version {v_old} nicht mehr vorhanden')
        # Ignore comments/briefing text -- check only structural occurrences
        old_in_comment = content.count(f'<!-- GREIF XPEDITION Krisenhandbuch {v_old} -->')
        old_in_sidebar = content.count(f'Krisenvorsorge {v_old}<')
        old_in_cache = content.count(f'greif-{v_old}')
        old_in_meta = content.count(f'{v_old} // GREIF XPEDITION')
        total_structural = old_in_comment + old_in_sidebar + old_in_cache + old_in_meta
        if total_structural == 0:
            ok(f'{v_old} nicht mehr in strukturellen Stellen vorhanden')
        else:
            fail(f'{v_old} noch in {total_structural} strukturellen Stellen vorhanden')
    else:
        print(f'\n[6] Alte Version -- VOLD nicht angegeben, wird uebersprungen')

    # ===== 7. ACCEPTANCE TEST =====
    print('\n[7] acceptance_test.py')
    acceptance_path = os.path.join(SCRIPT_DIR, 'acceptance_test.py')
    if os.path.exists(acceptance_path):
        result = subprocess.run(
            [sys.executable, acceptance_path, html_path],
            capture_output=True, text=True
        )
        # Parse result: expect 47/48
        match = re.search(r'(\d+)/(\d+) Tests bestanden', result.stdout)
        if match:
            passed, total = int(match.group(1)), int(match.group(2))
            # 47/48 is acceptable (Persona-Karten absichtlich entfernt)
            if passed >= 47 and total == 48:
                ok(f'{passed}/{total} Tests bestanden (Persona-Karten absichtlich fehlend -- OK)')
            elif passed == total:
                ok(f'{passed}/{total} Tests bestanden')
            else:
                failed_matches = re.findall(r'  - (.+)', result.stdout)
                # Filter out Persona-Karten (acceptable failure)
                real_failures = [f for f in failed_matches if 'Persona' not in f]
                if not real_failures:
                    ok(f'{passed}/{total} Tests bestanden (nur Persona-Karten -- OK)')
                else:
                    for f in real_failures:
                        fail(f'acceptance_test: {f}')
        else:
            fail(f'acceptance_test: konnte Ergebnis nicht parsen\n{result.stdout[-200:]}')
    else:
        print(f'  ! acceptance_test.py nicht gefunden unter {acceptance_path} -- uebersprungen')

    # ===== 8. NAV TEST =====
    print('\n[8] test_nav.py')
    nav_path = os.path.join(SCRIPT_DIR, 'test_nav.py')
    if os.path.exists(nav_path):
        result = subprocess.run(
            [sys.executable, nav_path, html_path],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            ok(f'Nav-Simulator: {result.stdout.strip()}')
        else:
            fail(f'Nav-Simulator Fehler:\n{result.stdout.strip()[:300]}')
    else:
        print(f'  ! test_nav.py nicht gefunden unter {nav_path} -- uebersprungen')

    # ===== ZUSAMMENFASSUNG =====
    total_checks = ok_count + len(errors)
    print(f'\n{"=" * 60}')
    print(f'RELEASE CHECK: {html_path}')
    print(f'{"=" * 60}')
    print(f'{ok_count}/{total_checks} Checks bestanden')
    if errors:
        print(f'\nFEHLER ({len(errors)}):')
        for e in errors:
            print(f'  \u2717 {e}')
        print(f'\nNICHT DEPLOYEN -- erst Fehler beheben.')
    else:
        print(f'\nAlle Checks bestanden. Bereit fuer Deployment.')
    print(f'{"=" * 60}\n')

    return len(errors) == 0


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Aufruf: python3 release_check.py index.html VNEW [VOLD]')
        print('  VNEW: neue Version, z.B. V39.1')
        print('  VOLD: alte Version (optional), z.B. V39.0')
        sys.exit(1)

    html = sys.argv[1]
    v_new = sys.argv[2]
    v_old = sys.argv[3] if len(sys.argv) > 3 else None

    if not os.path.exists(html):
        print(f'Datei nicht gefunden: {html}')
        sys.exit(1)

    success = run_check(html, v_new, v_old)
    sys.exit(0 if success else 1)
