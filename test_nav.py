#!/usr/bin/env python3
"""
Nav-Simulator: prueft Konsistenz zwischen Sidebar, Section-IDs und JS-Maps.
Wird vom release_check.py aufgerufen.
"""
import re
import sys
from bs4 import BeautifulSoup


def simulate_nav(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')

    # Alle Section-IDs sammeln
    section_ids = {s['id'] for s in soup.find_all('section', id=True)}
    div_ids = set(re.findall(r'<div[^>]+id="([^"]+)"', content))
    all_ids = section_ids | div_ids

    errors = []

    # Sidebar parsen
    sidebar_start = content.find('<nav id="sidebar"')
    sidebar_end = content.find('</nav>', sidebar_start)
    sidebar = content[sidebar_start:sidebar_end]

    # Alle data-id Links in der Sidebar pruefen
    sidebar_links = re.findall(r'data-id="([^"]+)"', sidebar)
    for link in sidebar_links:
        if link not in all_ids:
            errors.append(f"\u2717 Sidebar-Link 'data-id={link}' zeigt auf nicht-existente Section")

    # Alle Gruppen-IDs sammeln
    group_ids = set(re.findall(r'id="(ng-[^"]+)"', sidebar))

    # Map-Pruefung
    for map_name in ['const map = {', 'const _navGroupMap = {']:
        pos = content.find(map_name)
        if pos == -1:
            errors.append(f"\u2717 {map_name} nicht gefunden")
            continue
        map_text = content[pos:pos + 5000]
        # Nur Eintraege bis zur schliessenden Klammer
        end = map_text.find('};')
        if end > 0:
            map_text = map_text[:end]
        mapped_pairs = re.findall(r"'([^']+)':\s*'(ng-[^']+)'", map_text)
        for sec_id, group_id in mapped_pairs:
            if sec_id not in all_ids:
                errors.append(f"\u2717 {map_name.strip()} mapped '{sec_id}' (Section existiert nicht)")
            if group_id not in group_ids:
                errors.append(f"\u2717 {map_name.strip()} mapped auf '{group_id}' (Gruppe existiert nicht)")

    # Interne href-Links pruefen (ohne Script-Bloecke)
    html_only = re.sub(r'<script[\s\S]*?</script>', '', content)
    href_links = re.findall(r'href="#([^"${\s]+)"', html_only)
    for href in set(href_links):
        if href.startswith('${'):
            continue
        if href not in all_ids:
            errors.append(f"\u2717 href=#{href} zeigt ins Leere")

    if errors:
        print("Nav-Simulator Fehler:")
        for e in errors:
            print(f"  {e}")
        return False

    print(f"Nav-Simulator OK: {len(all_ids)} IDs, {len(sidebar_links)} Sidebar-Links, {len(group_ids)} Gruppen")
    return True


if __name__ == '__main__':
    filepath = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/index.html'
    success = simulate_nav(filepath)
    sys.exit(0 if success else 1)
