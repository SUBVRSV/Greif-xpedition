# SSL-Problem greif-xpedition.subvrsv.de

## Problem
Die Domain greif-xpedition.subvrsv.de zeigt eine "unsichere Seite"-Warnung.
Aktueller Domain-Anbieter verlangt 80€/Jahr für SSL — nicht akzeptabel, da SSL seit Jahren kostenlos ist.

## Lösung: Cloudflare als kostenloser DNS + SSL

### Warum Cloudflare
- Kostenlos
- SSL automatisch über Let's Encrypt
- GitHub Pages funktioniert danach einwandfrei mit HTTPS
- Dauer ca. 30-60 Minuten
- Domain bleibt beim aktuellen Anbieter, nur Nameserver werden gewechselt

### Schritte
1. Kostenloses Konto erstellen auf https://cloudflare.com
2. Domain `subvrsv.de` hinzufügen
3. Cloudflare scannt vorhandene DNS-Einträge automatisch — prüfen ob alles übernommen wurde
4. Beim aktuellen Domain-Anbieter die Nameserver auf die von Cloudflare umstellen (Cloudflare zeigt die genauen Werte)
5. Warten bis DNS propagiert (30 Min bis 24h, meist schneller)
6. In GitHub → Repository → Settings → Pages: „Enforce HTTPS" aktivieren
7. Fertig — SSL-Zertifikat wird automatisch ausgestellt

### GitHub Pages Einstellungen prüfen
- https://github.com/subvrsv/Greif-xpedition/settings/pages
- Custom Domain: greif-xpedition.subvrsv.de ✓
- Enforce HTTPS: aktivieren sobald Cloudflare aktiv ist

### Alternative falls Cloudflare nicht gewünscht
Domain zu Hetzner, INWX, Netcup oder Porkbun umziehen.
Alle unter 15€/Jahr, SSL inklusive.
