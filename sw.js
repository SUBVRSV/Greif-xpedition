// GREIF XPEDITION Krisenhandbuch - Service Worker
const CACHE = 'greif-V27.0';

// Robuste URL-Erkennung: funktioniert auf GitHub Pages (Unterordner) und Root
const BASE = self.location.pathname.replace(/sw\.js$/, '');
const URLS = [
  BASE || '/',
  BASE + 'index.html',
  BASE + 'sw.js',
];

// Install: alle relevanten URLs cachen
self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(cache => {
      // addAll schlaegt fehl wenn eine URL nicht erreichbar ist
      // daher einzeln laden und Fehler ignorieren
      return Promise.allSettled(URLS.map(url => cache.add(url)));
    })
  );
  self.skipWaiting();
});

// Activate: alte Caches loeschen
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// Fetch: Network-first mit Cache-Fallback
// Strategie: immer frisch vom Netz versuchen, Cache als Backup
self.addEventListener('fetch', e => {
  if (e.request.mode !== 'navigate') return;

  e.respondWith(
    fetch(e.request)
      .then(res => {
        // Nur gueltige Antworten cachen
        if (res && res.status === 200 && res.type === 'basic') {
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone));
        }
        return res;
      })
      .catch(() => {
        // Offline: Cache-Fallback
        return caches.match(e.request)
          .then(cached => {
            if (cached) return cached;
            // Letzter Ausweg: Root aus Cache
            return caches.match(BASE || '/');
          });
      })
  );
});
