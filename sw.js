// Keeps a copy of the game for offline play. Network first: online you always
// get the latest files, and each one refreshes the copy; offline, the copy.
// Bump CACHE when SHELL changes, so the old copy is dropped.
const CACHE = 'sand-v1';
const SHELL = [
  './',
  './index.html',
  './manifest.webmanifest',
  './icon-192.png',
  './icon-512.png',
  './icon-maskable-512.png',
  './apple-touch-icon.png',
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const { request } = e;
  const isOwnGet = request.method === 'GET' && new URL(request.url).origin === self.location.origin;
  if (!isOwnGet) return;
  e.respondWith(
    fetch(request)
      .then(res => {
        if (res.ok) {
          const copy = res.clone();
          e.waitUntil(caches.open(CACHE).then(c => c.put(request, copy)));
        }
        return res;
      })
      .catch(async () => {
        const hit = await caches.match(request, { ignoreSearch: true });
        if (hit) return hit;
        if (request.mode === 'navigate') return caches.match('./');
        return Response.error();
      })
  );
});
