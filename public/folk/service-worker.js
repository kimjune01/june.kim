const CACHE = 'folklore-v14';
const CORE = ['/folk/', '/folk/manifest.webmanifest', '/folk/icon.svg'];

self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(CORE)));
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(key => key !== CACHE).map(key => caches.delete(key)))));
  self.clients.claim();
});

// The page HTML carries every story inline, so it goes network-first: deploys
// reach returning readers, and the cached copy only serves offline. Static
// assets stay cache-first.
self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET' || !new URL(event.request.url).pathname.startsWith('/folk/')) return;
  const isPage = event.request.mode === 'navigate' || new URL(event.request.url).pathname === '/folk/';
  if (isPage) {
    event.respondWith(fetch(event.request).then(response => {
      const copy = response.clone();
      caches.open(CACHE).then(cache => cache.put('/folk/', copy));
      return response;
    }).catch(() => caches.match('/folk/')));
    return;
  }
  event.respondWith(caches.match(event.request).then(cached => cached || fetch(event.request).then(response => {
    const copy = response.clone();
    caches.open(CACHE).then(cache => cache.put(event.request, copy));
    return response;
  }).catch(() => caches.match('/folk/'))));
});
