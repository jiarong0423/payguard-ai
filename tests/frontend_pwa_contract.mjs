import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import vm from 'node:vm';

import { canRegisterServiceWorker, serviceWorkerUrl, startPwa, INSTALL_SLOT_ID } from '../frontend/src/pwa.js';

const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const publicDir = resolve(projectRoot, 'frontend/public');
const workerSource = readFileSync(resolve(publicDir, 'sw.js'), 'utf8');
const ORIGIN = 'http://127.0.0.1:8000';

// ---- Service worker: load the real file into a sandbox with a recording fake browser. ----
function loadWorker({ shellHtml = '<script type="module" src="/assets/index-abc.js"></script><link rel="stylesheet" href="/assets/index-abc.css">' } = {}) {
  let online = true;
  const listeners = {};
  const fetches = [];
  const stores = new Map();
  const cacheOps = [];
  const makeCache = (name) => ({
    async match(request) { return stores.get(name)?.get(typeof request === 'string' ? request : new URL(request.url).pathname) ?? undefined; },
    async put(request, response) { cacheOps.push(['put', name, new URL(request.url).pathname]); stores.get(name).set(new URL(request.url).pathname, response); },
    async addAll(urls) { cacheOps.push(['addAll', name, [...urls]]); for (const url of urls) stores.get(name).set(url, new Response(`cached ${url}`)); },
  });
  const caches = {
    async open(name) { if (!stores.has(name)) stores.set(name, new Map()); return makeCache(name); },
    async keys() { return [...stores.keys()]; },
    async delete(name) { cacheOps.push(['delete', name]); return stores.delete(name); },
    async match(path) { for (const store of stores.values()) if (store.has(path)) return store.get(path); return undefined; },
  };
  const fakeFetch = async (input, init) => {
    const url = typeof input === 'string' ? new URL(input, ORIGIN).href : input.url;
    fetches.push(url);
    if (!online) throw new TypeError('Failed to fetch');
    if (new URL(url).pathname === '/') return new Response(shellHtml, { status: 200 });
    const response = new Response(`network ${url}`, { status: 200 });
    Object.defineProperty(response, 'type', { value: 'basic' });
    return response;
  };
  const self = {
    location: new URL(`${ORIGIN}/sw.js?v=index-abc`),
    addEventListener(type, handler) { (listeners[type] ||= []).push(handler); },
    skipWaiting: async () => {},
    clients: { claim: async () => {} },
  };
  const context = vm.createContext({ self, caches, fetch: fakeFetch, URL, Response, Promise, Set, Error, TypeError, Object, decodeURIComponent });
  vm.runInContext(workerSource, context, { filename: 'sw.js' });
  return { context, listeners, fetches, cacheOps, stores, self, setOnline(value) { online = value; } };
}

function request(path, { method = 'GET', mode = 'cors', origin = ORIGIN } = {}) {
  return { url: path.startsWith('http') ? path : `${origin}${path}`, method, mode, headers: {} };
}

async function dispatchFetch(worker, req) {
  let responded = null;
  const event = { request: req, respondWith(value) { assert.equal(responded, null, 'respondWith called twice'); responded = Promise.resolve(value); } };
  for (const handler of worker.listeners.fetch) handler(event);
  return responded;
}

async function runLifecycle(worker, type) {
  const waits = [];
  for (const handler of worker.listeners[type] || []) handler({ waitUntil: (promise) => waits.push(promise) });
  await Promise.all(waits);
}

{
  const worker = loadWorker();
  assert.ok(worker.listeners.fetch?.length === 1, 'sw.js registers exactly one fetch handler');

  // 1. /api/ is never intercepted, whatever the method, mode, casing, encoding or slash form.
  const apiPaths = [
    '/api/', '/api', '/api/v1/health', '/api/v1/session', '/api/v1/paypal/disputes?x=1', '/api/v1/ai/brief#frag',
    '/API/v1/health', '/Api/v1/session', '/%61pi/v1/health', '/%2561pi/v1/health', '/api%2Fv1/health', '//api/v1/health',
    '/api\\v1\\health', '/%E0%A4%A/api', '/./api/v1/health', '/assets/../api/v1/health',
  ];
  const modes = ['cors', 'same-origin', 'no-cors', 'navigate'];
  const methods = ['GET', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'];
  for (const path of apiPaths) {
    for (const mode of modes) {
      for (const method of methods) {
        const responded = await dispatchFetch(worker, request(path, { method, mode }));
        assert.equal(responded, null, `sw.js must not handle ${method} ${path} (${mode})`);
      }
    }
    assert.equal(worker.context.isApiPath(new URL(`${ORIGIN}${path}`).pathname), true, `isApiPath(${path})`);
  }
  // Also when the API is reached through the other allowed loopback names.
  for (const origin of ['http://localhost:8000', 'http://[::1]:8000', 'http://127.0.0.1:5173']) {
    assert.equal(await dispatchFetch(worker, request('/api/v1/health', { origin })), null);
  }
  assert.deepEqual(worker.fetches, [], 'no network request is started for /api/');
  assert.deepEqual(worker.cacheOps, [], 'nothing is cached for /api/');

  // 2. Non-GET and cross-origin requests are left alone; no third-party fetches.
  assert.equal(await dispatchFetch(worker, request('/assets/index-abc.js', { method: 'POST' })), null);
  assert.equal(await dispatchFetch(worker, request('https://example.com/assets/x.js')), null);
  assert.equal(await dispatchFetch(worker, request('https://example.com/', { mode: 'navigate' })), null);
  // Unknown same-origin non-navigation paths are not intercepted either.
  assert.equal(await dispatchFetch(worker, request('/something.json')), null);
  assert.doesNotMatch(workerSource, /https?:\/\//, 'sw.js names no absolute URL (no third-party or new network endpoints)');
  assert.doesNotMatch(workerSource, /importScripts|workbox/i, 'sw.js loads no external code');
}

// 3. Install precaches the shell (offline page, manifest, icons, hashed assets) and never /api/.
{
  const worker = loadWorker({ shellHtml: '<script src="/assets/index-abc.js"></script><link href="/assets/index-abc.css"><a href="/api/v1/health"></a>' });
  await runLifecycle(worker, 'install');
  const addAll = worker.cacheOps.find(([op]) => op === 'addAll');
  assert.ok(addAll, 'install calls cache.addAll');
  assert.equal(addAll[1], 'payguard-shell-index-abc', 'cache name carries the build version from the registration URL');
  // (S26 2026-11-12) The offline page's two self-hosted fonts are precached too, so it keeps the console's type offline.
  for (const url of ['/offline.html', '/manifest.webmanifest', '/icons/icon-192.png', '/icons/icon-512.png', '/icons/icon-maskable-512.png', '/fonts/Newsreader-latin-var.woff2', '/fonts/PublicSans-latin-var.woff2', '/assets/index-abc.js', '/assets/index-abc.css']) {
    assert.ok(addAll[2].includes(url), `precache includes ${url}`);
  }
  assert.ok(addAll[2].every((url) => !/^\/+api/i.test(url)), 'precache never contains /api/');
  assert.deepEqual(worker.fetches, [`${ORIGIN}/`], 'install fetches only the same-origin shell page');

  // Activate removes older shell caches only.
  worker.stores.set('payguard-shell-old', new Map());
  worker.stores.set('someone-else', new Map());
  await runLifecycle(worker, 'activate');
  assert.deepEqual([...worker.stores.keys()].sort(), ['payguard-shell-index-abc', 'someone-else']);

  // Cached assets are served from cache; uncached hashed assets are fetched once and stored.
  const cachedAsset = await dispatchFetch(worker, request('/assets/index-abc.js'));
  assert.equal(await (await cachedAsset).text(), 'cached /assets/index-abc.js');
  const lazy = await dispatchFetch(worker, request('/assets/GuideReplay-xyz.js'));
  assert.equal(await (await lazy).text(), `network ${ORIGIN}/assets/GuideReplay-xyz.js`);
  assert.ok(worker.cacheOps.some(([op, , path]) => op === 'put' && path === '/assets/GuideReplay-xyz.js'));
  assert.ok(worker.cacheOps.filter(([op]) => op === 'put').every(([, , path]) => path.startsWith('/assets/')), 'runtime cache stores /assets/ only');
}

// 4. Navigation: network first; the offline page when the local server cannot be reached.
{
  const worker = loadWorker();
  await runLifecycle(worker, 'install');
  const page = await dispatchFetch(worker, request('/', { mode: 'navigate' }));
  assert.equal((await page).status, 200);
  assert.deepEqual(worker.fetches.slice(-1), [`${ORIGIN}/`], 'navigation goes to the network first');
  // A non-root navigation also falls back to the offline page, never to a cached API answer.
  const offlineWorker = loadWorker();
  await runLifecycle(offlineWorker, 'install');
  offlineWorker.setOnline(false);
  const offline = await dispatchFetch(offlineWorker, request('/', { mode: 'navigate' }));
  assert.equal(await (await offline).text(), 'cached /offline.html');
}

// 5. Offline page says the console cannot reach its API, explains the hosted wake-up and the local start, and loads nothing from elsewhere.
{
  const offlineHtml = readFileSync(resolve(publicDir, 'offline.html'), 'utf8');
  assert.match(offlineHtml, /cannot reach its API/);
  assert.match(offlineHtml, /tools\/run\.sh console/);
  assert.doesNotMatch(offlineHtml, /<script|src="https?:|href="https?:/i);
  // (S26 2026-11-12) Console look: newsprint canvas, square ink button, Newsreader + Public Sans from /fonts, a Phosphor icon,
  // the toast's wording; the old blue button, white card and blue shield image are gone.
  assert.match(offlineHtml, /--canvas: #f1ede3;/);
  assert.match(offlineHtml, /url\('\/fonts\/Newsreader-latin-var\.woff2'\)/);
  assert.match(offlineHtml, /url\('\/fonts\/PublicSans-latin-var\.woff2'\)/);
  assert.match(offlineHtml, /Nothing was sent/);
  assert.doesNotMatch(offlineHtml, /#2563eb|#f8fafc|border-radius|icon-192\.png/i);
  for (const font of ['Newsreader-latin-var.woff2', 'PublicSans-latin-var.woff2']) assert.ok(existsSync(resolve(publicDir, 'fonts', font)), `${font} ships in public/fonts`);
}

// 6. Manifest contract.
{
  const manifest = JSON.parse(readFileSync(resolve(publicDir, 'manifest.webmanifest'), 'utf8'));
  assert.equal(manifest.start_url, '/');
  assert.equal(manifest.display, 'standalone');
  assert.match(manifest.theme_color, /^#[0-9a-f]{6}$/i);
  const sizes = (purpose) => manifest.icons.filter((icon) => icon.purpose.split(' ').includes(purpose)).map((icon) => icon.sizes);
  assert.ok(sizes('any').includes('192x192') && sizes('any').includes('512x512'));
  assert.ok(sizes('maskable').includes('512x512'));
  for (const icon of manifest.icons) {
    const png = readFileSync(resolve(publicDir, icon.src.slice(1)));
    assert.equal(png.subarray(1, 4).toString('ascii'), 'PNG', `${icon.src} is a PNG`);
    const [width, height] = [png.readUInt32BE(16), png.readUInt32BE(20)];
    assert.equal(`${width}x${height}`, icon.sizes, `${icon.src} has the declared size`);
  }
}

// 7. Registration gate: production builds only, and only on secure contexts or loopback hosts.
{
  const base = { production: true, supported: true, secureContext: false, hostname: '127.0.0.1' };
  assert.equal(canRegisterServiceWorker(base), true);
  assert.equal(canRegisterServiceWorker({ ...base, hostname: 'localhost' }), true);
  assert.equal(canRegisterServiceWorker({ ...base, production: false }), false);
  assert.equal(canRegisterServiceWorker({ ...base, production: undefined }), false);
  assert.equal(canRegisterServiceWorker({ ...base, supported: false }), false);
  assert.equal(canRegisterServiceWorker({ ...base, hostname: '192.168.1.20' }), false);
  assert.equal(canRegisterServiceWorker({ ...base, hostname: '192.168.1.20', secureContext: true }), true);
  assert.equal(serviceWorkerUrl('http://127.0.0.1:8000/assets/index-CGMbaCN1.js'), '/sw.js?v=index-CGMbaCN1');
  assert.equal(serviceWorkerUrl('not a url'), '/sw.js?v=unversioned');
  assert.equal(serviceWorkerUrl('http://127.0.0.1:8000/assets/<bad>.js'), '/sw.js?v=unversioned');

  const registered = [];
  const listeners = {};
  const fakeWindow = (overrides) => ({
    isSecureContext: true,
    location: { hostname: '127.0.0.1' },
    navigator: { serviceWorker: { register: async (url, options) => { registered.push([url, options]); } } },
    document: { readyState: 'complete', getElementById: () => null, body: {} },
    addEventListener: (type, handler) => { (listeners[type] ||= []).push(handler); },
    ...overrides,
  });
  assert.equal(startPwa({ production: false, win: fakeWindow() }), false);
  assert.equal(startPwa({ win: fakeWindow() }), false, 'production must be explicit');
  assert.deepEqual(registered, []);
  assert.deepEqual(listeners, {}, 'development builds add no listeners');
  assert.equal(startPwa({ production: true, win: fakeWindow(), moduleUrl: 'http://127.0.0.1:8000/assets/index-abc.js' }), true);
  await Promise.resolve();
  assert.deepEqual(registered, [['/sw.js?v=index-abc', { scope: '/' }]]);
  assert.ok(listeners.beforeinstallprompt && listeners.appinstalled);
  assert.equal(INSTALL_SLOT_ID, 'pwa-install-slot');
}

// 8. The top bar exposes the install slot pwa.js looks for.
{
  const app = readFileSync(resolve(projectRoot, 'frontend/src/App.jsx'), 'utf8');
  assert.match(app, /<header className="topbar"[\s\S]*id="pwa-install-slot"[\s\S]*<\/header>/);
}

console.log('frontend PWA contract: ok');
