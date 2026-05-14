#!/usr/bin/env python3
"""
linkrot_check.py -- GREIF XPEDITION Krisenhandbuch
Prueft alle externen Links in index.html auf Erreichbarkeit.

Verwendung:
  python3 linkrot_check.py index.html
  python3 linkrot_check.py index.html --timeout 10
  python3 linkrot_check.py index.html --output report.txt
  python3 linkrot_check.py index.html --only-errors

Hinweis: HTTP 403 von bekannten Seiten (Amazon, Instagram, etc.) ist meist
Bot-Schutz, kein echter Linkrot. Das Skript kennzeichnet diese als WARN statt FEHLER.
DNS-Fehler und HTTP 404/410 sind echte Linkrot-Kandidaten.
"""

import sys
import re
import urllib.request
import urllib.error
import urllib.parse
import ssl
import argparse
import time
from collections import defaultdict

# Domains die 403 fuer Bots zurueckgeben aber erreichbar sind
BOT_BLOCK_DOMAINS = {
    'amazon.de', 'amazon.com', 'www.amazon.de', 'www.amazon.com',
    'instagram.com', 'www.instagram.com',
    'signal.org', 'www.signal.org',
    'osmand.net', 'www.osmand.net',
    'organicmaps.app', 'www.organicmaps.app',
    'radio.garden', 'www.radio.garden',
    'inaturalist.org', 'www.inaturalist.org',
    'zello.com', 'www.zello.com',
    'komoot.com', 'www.komoot.com',
    'windy.com', 'www.windy.com',
    'bbk.bund.de', 'www.bbk.bund.de',
    'archive.org', 'www.archive.org',
    'wildnisschule-lupus.de', 'www.wildnisschule-lupus.de',
    'dwd.de', 'www.dwd.de',
    'animatedknots.com', 'www.animatedknots.com',
    'nabu.de', 'www.nabu.de',
    'katwarn.de', 'www.katwarn.de',
    'identify.plantnet.org',
    'kostbarenatur.net', 'www.kostbarenatur.net',
    'saurugg.net', 'www.saurugg.net',
    'globetrotter.de', 'www.globetrotter.de',
    'tacwrk.com', 'www.tacwrk.com',
    'bw-online-shop.com', 'www.bw-online-shop.com',
    'asmc.de', 'www.asmc.de',
    'camostore.de', 'www.camostore.de',
    'krusche-outdoor.de', 'www.krusche-outdoor.de',
    'backpacker-wilderness.com', 'www.backpacker-wilderness.com',
}

def extract_links(html_path):
    with open(html_path, encoding='utf-8') as f:
        content = f.read()

    pattern = r'(?:href|src)=["\']([^"\']+)["\']'
    raw = re.findall(pattern, content)

    links = []
    seen = set()
    for url in raw:
        url = url.strip()
        if url in seen:
            continue
        seen.add(url)
        if url.startswith(('#', 'data:', 'javascript:', 'mailto:', 'tel:')):
            links.append((url, 'SKIP'))
        elif url.startswith('http://') or url.startswith('https://'):
            links.append((url, 'CHECK'))
        else:
            links.append((url, 'SKIP'))

    return links

def encode_url(url):
    """URL-encode Umlaute und Sonderzeichen im Pfad/Query-Teil."""
    try:
        parsed = urllib.parse.urlparse(url)
        # Nur Pfad und Query encoden, nicht Host
        encoded_path = urllib.parse.quote(parsed.path, safe='/:@!$&\'()*+,;=')
        encoded_query = urllib.parse.quote(parsed.query, safe='=&+%:@!$\'()*,;/?')
        rebuilt = urllib.parse.urlunparse((
            parsed.scheme, parsed.netloc, encoded_path,
            parsed.params, encoded_query, parsed.fragment
        ))
        return rebuilt
    except Exception:
        return url

def is_bot_blocked(url, code):
    """Gibt True wenn 403 vermutlich Bot-Schutz ist, nicht echter Fehler."""
    if code != 403:
        return False
    try:
        host = urllib.parse.urlparse(url).netloc.lower()
        return host in BOT_BLOCK_DOMAINS
    except Exception:
        return False

def check_url(url, timeout=8):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    safe_url = encode_url(url)
    req = urllib.request.Request(
        safe_url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,*/*;q=0.8',
            'Accept-Language': 'de-DE,de;q=0.9',
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            code = resp.status
            if 200 <= code < 300:
                return code, 'OK'
            elif 300 <= code < 400:
                return code, 'OK'  # Redirect = erreichbar
            else:
                if is_bot_blocked(url, code):
                    return code, 'WARN-BOTBLOCK'
                return code, 'FEHLER'
    except urllib.error.HTTPError as e:
        if is_bot_blocked(url, e.code):
            return e.code, 'WARN-BOTBLOCK'
        return e.code, 'FEHLER'
    except urllib.error.URLError as e:
        reason = str(e.reason)
        if 'Name or service not known' in reason or 'nodename nor servname' in reason:
            return None, 'DNS-FEHLER'
        return None, f'FEHLER ({reason[:40]})'
    except Exception as e:
        return None, f'FEHLER ({type(e).__name__})'

def main():
    parser = argparse.ArgumentParser(description='Linkrot-Checker fuer GREIF XPEDITION')
    parser.add_argument('html', help='Pfad zu index.html')
    parser.add_argument('--timeout', type=int, default=8, help='Timeout in Sekunden (default: 8)')
    parser.add_argument('--output', help='Ergebnisse in Datei schreiben')
    parser.add_argument('--only-errors', action='store_true', help='Nur Fehler und Warnungen ausgeben')
    args = parser.parse_args()

    links = extract_links(args.html)
    to_check = [(url, kind) for url, kind in links if kind == 'CHECK']
    skipped = [(url, kind) for url, kind in links if kind == 'SKIP']

    print(f"GREIF XPEDITION Linkrot-Check")
    print(f"Datei: {args.html}")
    print(f"Links gesamt: {len(links)} | Zu pruefen: {len(to_check)} | Uebersprungen: {len(skipped)}")
    print(f"Timeout: {args.timeout}s")
    print(f"Hinweis: WARN-BOTBLOCK = Site erreichbar aber blockiert Bots (kein Linkrot)")
    print("-" * 70)

    results = []
    stats = defaultdict(int)

    for i, (url, _) in enumerate(to_check):
        sys.stdout.write(f"\r[{i+1}/{len(to_check)}] {url[:65]:<65}")
        sys.stdout.flush()
        t0 = time.time()
        code, status = check_url(url, args.timeout)
        elapsed = time.time() - t0
        results.append((url, code, status, elapsed))
        stats[status] += 1
        time.sleep(0.2)

    print()
    print("=" * 70)
    print("ERGEBNISSE")
    print("=" * 70)

    lines_out = []
    # Sortierung: Fehler zuerst, dann Warnungen, dann OK
    priority = {'DNS-FEHLER': 0, 'FEHLER': 1, 'WARN': 2, 'WARN-BOTBLOCK': 3, 'OK': 4}
    sorted_results = sorted(results, key=lambda x: priority.get(x[2].split('(')[0], 5))

    for url, code, status, elapsed in sorted_results:
        if args.only_errors and status in ('OK', 'WARN-BOTBLOCK'):
            continue
        code_str = str(code) if code else '---'
        line = f"{status:<18} [{code_str:>3}] ({elapsed:.1f}s)  {url}"
        print(line)
        lines_out.append(line)

    print()
    print("ZUSAMMENFASSUNG:")
    for s in ['OK', 'WARN', 'WARN-BOTBLOCK', 'DNS-FEHLER', 'FEHLER']:
        count = stats.get(s, 0)
        if count > 0:
            label = {
                'OK': 'OK (erreichbar)',
                'WARN': 'WARN (unerwarteter Status)',
                'WARN-BOTBLOCK': 'WARN-BOTBLOCK (Site OK, blockiert Bots)',
                'DNS-FEHLER': 'DNS-FEHLER (Domain nicht aufloesbar -- LINKROT-KANDIDAT)',
                'FEHLER': 'FEHLER (HTTP 4xx/5xx oder Timeout -- pruefen)',
            }.get(s, s)
            print(f"  {label}: {count}")
    print(f"  SKIP: {len(skipped)} (Anker, data:, mailto:, relative URLs)")

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines_out))
            f.write("\n\nSUMMARY:\n")
            for s, count in stats.items():
                f.write(f"  {s}: {count}\n")
        print(f"\nReport gespeichert: {args.output}")

    echte_fehler = stats.get('DNS-FEHLER', 0) + stats.get('FEHLER', 0)
    if echte_fehler > 0:
        print(f"\n{echte_fehler} pruefwuerdige Links (DNS-Fehler oder HTTP-Fehler).")
        print("Bot-geblockte Sites (WARN-BOTBLOCK) sind kein Linkrot.")
        sys.exit(1)
    else:
        print(f"\nKein echter Linkrot gefunden.")

if __name__ == '__main__':
    main()
