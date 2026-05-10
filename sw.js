// GREIF XPEDITION Krisenhandbuch - Service Worker
const CACHE = 'greif-V38.5';

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

// Fetch: Stale-While-Revalidate
// Strategie: aus Cache servieren wenn vorhanden (instant), parallel Netzwerk-Update
// Wenn neue Version da: beim nächsten Load nutzbar
self.addEventListener('fetch', e => {
  if (e.request.mode !== 'navigate') return;

  e.respondWith(
    caches.open(CACHE).then(cache =>
      cache.match(e.request).then(cached => {
        const networkFetch = fetch(e.request).then(res => {
          // Nur gueltige Antworten cachen
          if (res && res.status === 200 && res.type === 'basic') {
            cache.put(e.request, res.clone());
          }
          return res;
        }).catch(() => cached || cache.match(BASE || '/'));

        // Cache zuerst (instant), Netz im Hintergrund fuer naechstes Mal
        return cached || networkFetch;
      })
    )
  );
});

