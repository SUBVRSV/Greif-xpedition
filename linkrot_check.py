#!/usr/bin/env python3
"""
Linkrot-Checker fuer GREIF XPEDITION Krisenhandbuch
Prueft alle externen Links auf Erreichbarkeit.
Aufruf: python3 linkrot_check.py index.html [--timeout 10]
"""

import sys
import re
import time
import argparse
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

def extract_links(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    # Alle href="http..." Links
    links = re.findall(r'href="(https?://[^"]+)"', content)
    # Deduplizieren aber Reihenfolge behalten
    seen = set()
    unique = []
    for l in links:
        if l not in seen:
            seen.add(l)
            unique.append(l)
    return unique

def check_link(url, timeout=10):
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (compatible; LinkChecker/1.0)',
                'Accept': 'text/html,application/xhtml+xml,*/*'
            }
        )
        resp = urllib.request.urlopen(req, timeout=timeout)
        code = resp.getcode()
        return (url, code, 'OK' if code < 400 else 'FEHLER')
    except urllib.error.HTTPError as e:
        return (url, e.code, 'HTTP-FEHLER')
    except urllib.error.URLError as e:
        return (url, 0, f'NICHT ERREICHBAR: {e.reason}')
    except Exception as e:
        return (url, 0, f'FEHLER: {e}')

def main():
    parser = argparse.ArgumentParser(description='Linkrot-Checker')
    parser.add_argument('filepath', help='Pfad zur index.html')
    parser.add_argument('--timeout', type=int, default=10, help='Timeout in Sekunden (Standard: 10)')
    parser.add_argument('--workers', type=int, default=8, help='Parallele Verbindungen (Standard: 8)')
    args = parser.parse_args()

    links = extract_links(args.filepath)
    print(f'\nGREIF XPEDITION Linkrot-Checker')
    print(f'================================')
    print(f'{len(links)} externe Links gefunden. Pruefe...\n')

    results = []
    start = time.time()

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(check_link, url, args.timeout): url for url in links}
        done = 0
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            done += 1
            status = result[2]
            marker = '  OK' if 'OK' in status else 'FAIL'
            print(f'[{done:3d}/{len(links)}] {marker}  {result[0][:80]}')

    elapsed = time.time() - start

    # Auswertung
    ok = [r for r in results if 'OK' in r[2]]
    fail = [r for r in results if 'OK' not in r[2]]

    print(f'\n================================')
    print(f'Ergebnis nach {elapsed:.1f}s:')
    print(f'  Erreichbar:     {len(ok):3d}')
    print(f'  Nicht erreichbar: {len(fail):3d}')
    print()

    if fail:
        print('FEHLGESCHLAGENE LINKS:')
        for url, code, status in sorted(fail, key=lambda x: x[2]):
            print(f'  [{code}] {status}')
            print(f'       {url}')
        print()
        sys.exit(1)
    else:
        print('Alle Links erreichbar.')
        sys.exit(0)

if __name__ == '__main__':
    main()
