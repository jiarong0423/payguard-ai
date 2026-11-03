/*
 * PayGuard console service worker. Hand-written, no dependencies.
 *
 * What it does:
 *   - On install, precaches the built shell: the offline page, the web manifest, the icons and
 *     the /assets/ files that the freshly fetched index.html references.
 *   - Page navigations go to the network first; when the local server cannot be reached, the
 *     precached offline page explains that the console needs the local API.
 *   - Hashed /assets/ files are served cache-first (their names change with every build).
 *
 * What it never does:
 *   - It never handles, caches or rewrites /api/ requests (any method, any casing, percent-encoded
 *     or not). Those go straight to the browser's network stack as if no worker existed.
 *   - It never handles non-GET requests or requests to other origins, and it starts no network
 *     request of its own except the same-origin shell fetch during install.
 */
'use strict';

const CACHE_PREFIX = 'payguard-shell-';
const OFFLINE_URL = '/offline.html';
const STATIC_SHELL = Object.freeze([
  OFFLINE_URL,
  '/manifest.webmanifest',
  '/icons/icon.svg',
  '/icons/icon-192.png',
  '/icons/icon-512.png',
  '/icons/icon-maskable-512.png',
  '/icons/apple-touch-icon.png',
]);
const SHELL_ASSET_PATTERN = /(?:src|href)="(\/assets\/[A-Za-z0-9._-]+)"/g;

function buildVersion(scriptUrl) {
  let version = '';
  try { version = new URL(scriptUrl).searchParams.get('v') || ''; } catch { version = ''; }
  return /^[A-Za-z0-9_-]{1,64}$/.test(version) ? version : 'unversioned';
}

const CACHE_NAME = CACHE_PREFIX + buildVersion(self.location.href);

// True for every path the API could answer, and then some: any casing, repeated slashes, and every
// percent-decoded form (the server decodes escapes before routing). Undecodable paths count as API,
// so they are left alone too.
function isApiPath(pathname) {
  if (typeof pathname !== 'string') return true;
  let path = pathname;
  for (let round = 0; round < 4; round += 1) {
    if (/^[/\\]+api(?:[/\\]|$)/i.test(path)) return true;
    let decoded;
    try { decoded = decodeURIComponent(path); } catch { return true; }
    if (decoded === path) return false;
    path = decoded;
  }
  return true;
}

function shellPath(request) {
  if (!request || request.method !== 'GET') return null;
  let url;
  try { url = new URL(request.url); } catch { return null; }
  if (url.origin !== self.location.origin || isApiPath(url.pathname)) return null;
  return url.pathname;
}

// Decides whether this worker answers a request at all. Everything else is not intercepted.
function shouldHandle(request) {
  const path = shellPath(request);
  if (path === null) return false;
  if (request.mode === 'navigate') return true;
  return path.startsWith('/assets/') || STATIC_SHELL.includes(path);
}

async function shellUrls() {
  const response = await fetch('/', { cache: 'no-store', credentials: 'same-origin' });
  if (!response.ok) throw new Error('shell_unavailable');
  const html = await response.text();
  const assets = new Set();
  for (const match of html.matchAll(SHELL_ASSET_PATTERN)) {
    if (!isApiPath(match[1])) assets.add(match[1]);
  }
  return [...STATIC_SHELL, ...assets];
}

async function offlineResponse() {
  const cached = await caches.match(OFFLINE_URL);
  return cached || new Response('The PayGuard console needs the local API. Start it with ./tools/run.sh console.', {
    status: 503,
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  });
}

async function cacheFirst(request) {
  const cache = await caches.open(CACHE_NAME);
  const cached = await cache.match(request);
  if (cached) return cached;
  const response = await fetch(request);
  if (response.ok && response.type === 'basic' && new URL(request.url).pathname.startsWith('/assets/')) {
    await cache.put(request, response.clone());
  }
  return response;
}

self.addEventListener('install', (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE_NAME);
    await cache.addAll(await shellUrls());
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', (event) => {
  event.waitUntil((async () => {
    const names = await caches.keys();
    await Promise.all(names.filter((name) => name.startsWith(CACHE_PREFIX) && name !== CACHE_NAME).map((name) => caches.delete(name)));
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (!shouldHandle(request)) return;
  if (request.mode === 'navigate') {
    event.respondWith(fetch(request).catch(() => offlineResponse()));
    return;
  }
  event.respondWith(cacheFirst(request));
});
