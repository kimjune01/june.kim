// Pinyin Chart - Service Worker for Audio Caching
// This service worker intercepts audio requests and caches them for offline use

const CACHE_NAME = 'pinyin-audio-v1';
const STATIC_CACHE = 'pinyin-static-v1';

// Audio CDN hostnames to cache
const AUDIO_HOSTS = ['jsdelivr.net', 'githubusercontent.com'];

// Install event - setup caches
self.addEventListener('install', (event) => {
  console.log('[SW] Installing service worker...');

  event.waitUntil(
    caches.open(STATIC_CACHE).then((cache) => {
      console.log('[SW] Static cache opened');
      // Optionally precache critical assets here
      return cache.addAll([
        '/pinyin-chart/favicon.svg'
      ]);
    })
  );

  // Force the waiting service worker to become the active service worker
  self.skipWaiting();
});

// Activate event - cleanup old caches
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating service worker...');

  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          // Delete old caches
          if (cacheName !== CACHE_NAME && cacheName !== STATIC_CACHE) {
            console.log('[SW] Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );

  // Take control of all pages immediately
  return self.clients.claim();
});

// Fetch event - intercept and cache audio requests
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // Only cache audio files from our CDN hosts
  const isAudioRequest = AUDIO_HOSTS.some(host => url.hostname.includes(host)) &&
                         url.pathname.endsWith('.mp3');

  if (isAudioRequest) {
    // Cache-first strategy for audio files
    event.respondWith(
      caches.match(event.request).then((cachedResponse) => {
        if (cachedResponse) {
          console.log('[SW] Serving from cache:', url.pathname);
          return cachedResponse;
        }

        // Not in cache, fetch from network
        console.log('[SW] Fetching from network:', url.pathname);
        return fetch(event.request).then((response) => {
          // Check if we received a valid response
          if (!response || response.status !== 200 || response.type === 'error') {
            return response;
          }

          // Clone the response (can only be consumed once)
          const responseToCache = response.clone();

          // Cache for next time
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
            console.log('[SW] Cached audio file:', url.pathname);
          });

          return response;
        }).catch((error) => {
          console.error('[SW] Fetch failed for:', url.pathname, error);
          // Could return a fallback audio file here
          throw error;
        });
      })
    );
  } else {
    // For non-audio requests, just pass through to network
    event.respondWith(fetch(event.request));
  }
});

// Message event - handle commands from the app
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }

  if (event.data && event.data.type === 'GET_CACHE_SIZE') {
    // Calculate total cached audio files
    caches.open(CACHE_NAME).then((cache) => {
      cache.keys().then((keys) => {
        event.ports[0].postMessage({
          type: 'CACHE_SIZE',
          count: keys.length
        });
      });
    });
  }

  if (event.data && event.data.type === 'CLEAR_CACHE') {
    caches.delete(CACHE_NAME).then(() => {
      event.ports[0].postMessage({
        type: 'CACHE_CLEARED'
      });
    });
  }
});
