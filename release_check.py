from bs4 import BeautifulSoup
import re, sys, subprocess

def check(filepath, expected_version, prev_version):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')
    sections = soup.find_all('section', id=True)
    tables = soup.find_all('table')
    real_ids = {s['id'] for s in sections}
    div_ids = set(re.findall(r'<div[^>]+id="([^"]+)"', content))
    real_ids = real_ids | div_ids
    content_ids = {s['id'] for s in sections if s['id'] not in ('cover','inhalt')}

    sidebar_start = content.find('<nav id="sidebar"')
    sidebar_end = content.find('</nav>', sidebar_start)
    sidebar = content[sidebar_start:sidebar_end]
    actual_groups = set(re.findall(r'id="(ng-[^"]+)"', sidebar))

    results = []
    all_ok = True

    def chk(name, val, expected=None):
        nonlocal all_ok
        if expected is None:
            results.append(f"  \u2713 {name}: {val}")
        elif val == expected:
            results.append(f"  \u2713 {name}: {val}")
        else:
            results.append(f"  \u2717 {name}: {val} (erwartet {expected})")
            all_ok = False

    def fail(msg):
        nonlocal all_ok
        results.append(f"  \u2717 {msg}")
        all_ok = False

    def ok(msg):
        results.append(f"  \u2713 {msg}")

    chk('Kapitel', len(sections))
    chk('Tabellen', len(tables))
    chk('Em-Dashes', content.count('\u2014'), 0)

    opens = len(re.findall(r'<section id="', content))
    closes = len(re.findall(r'</section>', content))
    chk('Section balance', opens == closes, True)

    chk(f'Version {expected_version}', content.count(expected_version) >= 4, True)
    chk(f'Alte Version {prev_version} weg', content.count(prev_version), 0)

    for map_name in ['const map = {', 'const _navGroupMap = {']:
        pos = content.find(map_name)
        if pos == -1:
            fail(f"{map_name} NICHT GEFUNDEN")
            continue
        map_text = content[pos:pos+5000]
        mapped = set(re.findall(r"'([^']+)':\s*'ng-[^']+'", map_text))
        used_groups = set(re.findall(r"'(ng-[^']+)'", map_text))
        sidebar_s = content.find('<nav id="sidebar"')
        sidebar_e = content.find('</nav>', sidebar_s)
        sb = content[sidebar_s:sidebar_e]
        all_group_links = set()
        for gid in re.findall(r'id="(ng-[^"]+)"', sb):
            gs = sb.find(f'id="{gid}"')
            ge = sb.find('</div>\n  </div>', gs)
            all_group_links.update(re.findall(r'data-id="([^"]+)"', sb[gs:ge]))
        top_level = set(re.findall(r'data-id="([^"]+)"', sb)) - all_group_links
        missing = [rid for rid in content_ids if rid not in mapped and rid not in top_level]
        stale = [mid for mid in mapped if mid not in real_ids]
        bad_groups = sorted(used_groups - actual_groups)
        label = map_name.split('=')[0].strip()
        chk(f'{label} fehlend', missing, [])
        chk(f'{label} veraltet', stale, [])
        chk(f'{label} Gruppen existieren', bad_groups, [])

    # ── KRITISCHE FUNKTIONEN ──
    critical_fns = [
        'function _updateActiveNav',
        'const _allSections',
        'const _navGroupMap',
        'function navSearch',
        'function navTo',
        'function buildSearchIndex',
    ]
    for fn in critical_fns:
        chk(f'JS: {fn}', fn in content, True)

    # ── SUCHE: ID-KONSISTENZ ──
    search_input = re.search(r'<input[^>]+id="([^"]+)"[^>]*oninput="navSearch', content)
    nav_search_fn = content.find('function navSearch')
    if search_input and nav_search_fn > 0:
        fn_body = content[nav_search_fn:nav_search_fn+300]
        used_ids = re.findall(r"getElementById\('([^']+)'\)", fn_body)
        input_id = search_input.group(1)
        if used_ids and used_ids[0] != input_id and used_ids[0] not in ('nav-search-results',):
            fail(f"navSearch ID-Mismatch: sucht '{used_ids[0]}' aber Input ist '{input_id}'")
        else:
            ok(f"navSearch Input-ID korrekt ('{input_id}')")
    else:
        fail("navSearch: Input-Element oder Funktion nicht gefunden")

    # ── SUCHE: buildSearchIndex gibt Objekte mit .id und .title zurück ──
    bsi_pos = content.find('function buildSearchIndex(')
    if bsi_pos > 0:
        bsi_end = content.find("\nfunction ", bsi_pos + 10)
        bsi_body = content[bsi_pos:bsi_end]
        has_push_id = 'id:' in bsi_body or "'id'" in bsi_body or '"id"' in bsi_body
        has_push_title = 'title:' in bsi_body
        if has_push_id and has_push_title:
            ok("buildSearchIndex gibt {id, title} zurück")
        else:
            fail(f"buildSearchIndex: fehlende Felder (id:{has_push_id}, title:{has_push_title})")

    # ── SUCHE: navSearch nutzt buildSearchIndex ──
    ns_pos = content.find('function navSearch')
    ns_body = content[ns_pos:ns_pos+600]
    if 'buildSearchIndex' in ns_body:
        ok("navSearch ruft buildSearchIndex auf")
    else:
        fail("navSearch ruft buildSearchIndex NICHT auf")

    # ── SZENARIOPFAD-FUNKTIONEN ──
    szp_fns = ['szpShow', 'szpBannerUpdate', 'szpBannerNav', 'szpBannerClose', 'szpReset', 'szpSave', 'szpLoad']
    missing_szp = [f for f in szp_fns if f'function {f}' not in content]
    if missing_szp:
        fail(f"Fehlende Szenariopfad-Funktionen: {missing_szp}")
    else:
        ok(f"Alle {len(szp_fns)} Szenariopfad-Funktionen vorhanden")

    # ── WFM/KK-FUNKTIONEN ──
    other_fns = ['wfmRender', 'wfmInit', 'kkInit', 'kkRenderMonth', 'filterTag', 'applyFilter', 'printSection', 'openTool']
    missing_other = [f for f in other_fns if f'function {f}' not in content]
    if missing_other:
        fail(f"Fehlende Funktionen: {missing_other}")
    else:
        ok(f"Alle {len(other_fns)} weiteren Funktionen vorhanden")

    # ── JS-SYNTAX ──
    script_blocks = re.findall(r'<script>([\s\S]*?)</script>', content)
    syntax_ok = True
    for si, js in enumerate(script_blocks):
        in_s = in_d = esc = False
        i = 0
        while i < len(js):
            c = js[i]
            if not in_s and not in_d and js[i:i+2] == '//':
                while i < len(js) and js[i] != '\n': i += 1
                continue
            if not in_s and not in_d and js[i:i+2] == '/*':
                i += 2
                while i < len(js) and js[i-2:i] != '*/': i += 1
                continue
            if esc: esc = False; i += 1; continue
            if c == '\\': esc = True; i += 1; continue
            if not in_d and c == "'": in_s = not in_s
            elif not in_s and c == '"': in_d = not in_d
            i += 1
        if in_s or in_d:
            fail(f"JS Syntax Script {si}: unbalancierte Anführungszeichen")
            syntax_ok = False
    if syntax_ok:
        ok(f"JS-Syntax: alle {len(script_blocks)} Scripts OK")

    # ── INTERNE LINKS ──
    html_only = re.sub(r'<script[\s\S]*?</script>', '', content)
    internal_links = re.findall(r'href="#([^"${\s]+)"', html_only)
    broken = sorted(set(lid for lid in internal_links if lid not in real_ids and not lid.startswith('${')))
    chk('Interne Links gebrochen', broken, [])

    nav_data_ids = re.findall(r'data-id="([^"${\s]+)"', html_only)
    broken_nav = sorted(set(lid for lid in nav_data_ids if lid not in real_ids and not lid.startswith('${')))
    chk('Nav data-id gebrochen', broken_nav, [])

    # ── NAV-SIMULATOR ──
    nav_result = subprocess.run(
        ['python3', '/home/claude/test_nav.py', filepath],
        capture_output=True, text=True
    )
    if nav_result.returncode == 0:
        ok("Nav-Simulator: OK")
    else:
        fail("Nav-Simulator: FEHLER")
        for line in nav_result.stdout.split('\n'):
            if '\u2717' in line:
                results.append("    " + line.strip())

    # ── SCROLL-TO-TOP ──
    if "btn.classList.toggle('visible', window.scrollY > 400)" in content or \
       'classList.toggle(\'visible\'' in content:
        ok("Scroll-to-Top: Listener vorhanden")
    else:
        fail("Scroll-to-Top: Listener fehlt (Pfeil oben wird nie sichtbar)")

    # ── LIGHT MODE DEFAULT ──
    if '<body class="light-mode">' in content:
        ok("Light Mode: korrekt als Default gesetzt")
    else:
        fail("Light Mode: <body class='light-mode'> fehlt")

    print(f"\n=== RELEASE-CHECK {expected_version} ===\n")
    for r in results:
        print(r)
    errors = sum(1 for r in results if r.strip().startswith('\u2717'))
    status = 'ALLE CHECKS OK \u2014 RELEASE BEREIT' if all_ok else f'FEHLER ({errors}) \u2014 NICHT RELEASEN'
    print(f"\n{status}")
    print(f"Dateigr\u00f6sse: {len(content):,} Bytes\n")
    return all_ok

if __name__ == '__main__':
    filepath = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/index.html'
    version = sys.argv[2] if len(sys.argv) > 2 else 'V25.1'
    prev = sys.argv[3] if len(sys.argv) > 3 else 'V25.0'
    ok = check(filepath, version, prev)
    sys.exit(0 if ok else 1)
