// Progressive web app wiring: service worker registration and the top-bar install button.
// Nothing here runs in development builds, and nothing here starts a network request other than
// the browser fetching /sw.js from the same local origin.

export const LOOPBACK_HOSTS = Object.freeze(['127.0.0.1', 'localhost', '[::1]']);
export const INSTALL_SLOT_ID = 'pwa-install-slot';

export function canRegisterServiceWorker({ production, supported, secureContext, hostname }) {
  return production === true && supported === true && (secureContext === true || LOOPBACK_HOSTS.includes(hostname));
}

// The bundled module URL carries the build hash (for example /assets/index-CGMbaCN1.js). Passing it
// to the worker gives every build its own cache and makes the browser install the new worker.
export function serviceWorkerUrl(moduleUrl) {
  let name = '';
  try { name = new URL(moduleUrl).pathname.split('/').pop().replace(/\.[^.]*$/, ''); } catch { name = ''; }
  const version = /^[A-Za-z0-9_-]{1,64}$/.test(name) ? name : 'unversioned';
  return `/sw.js?v=${encodeURIComponent(version)}`;
}

function installButton(doc, onClick) {
  const button = doc.createElement('button');
  button.type = 'button';
  button.className = 'pwa-install-button';
  const svgNs = 'http://www.w3.org/2000/svg';
  const icon = doc.createElementNS(svgNs, 'svg');
  for (const [name, value] of Object.entries({ viewBox: '0 0 24 24', width: '18', height: '18', fill: 'none', stroke: 'currentColor', 'stroke-width': '1.8', 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'aria-hidden': 'true', focusable: 'false' })) icon.setAttribute(name, value);
  const path = doc.createElementNS(svgNs, 'path');
  path.setAttribute('d', 'M12 4v11m-4.5-4.5L12 15l4.5-4.5M5 19h14');
  icon.append(path);
  const label = doc.createElement('span');
  label.className = 'pwa-install-label';
  label.textContent = 'Install app';
  button.append(icon, label);
  button.setAttribute('aria-label', 'Install the TradeGlot console as an app');
  button.addEventListener('click', onClick);
  return button;
}

function watchInstallPrompt(win) {
  const doc = win.document;
  let deferredPrompt = null;
  let button = null;
  let observer = null;

  const hide = () => {
    observer?.disconnect();
    observer = null;
    button?.remove();
    button = null;
  };

  const attach = () => {
    const slot = doc.getElementById(INSTALL_SLOT_ID);
    if (!slot || !deferredPrompt) return false;
    if (!button) {
      button = installButton(doc, async () => {
        const prompt = deferredPrompt;
        deferredPrompt = null;
        hide();
        if (!prompt) return;
        await prompt.prompt();
        await prompt.userChoice.catch(() => null);
      });
    }
    if (button.parentNode !== slot) slot.append(button);
    return true;
  };

  const show = () => {
    if (attach()) return;
    // The prompt can arrive before React has rendered the top bar; wait for the slot.
    observer?.disconnect();
    observer = new win.MutationObserver(() => {
      if (attach()) { observer.disconnect(); observer = null; }
    });
    observer.observe(doc.body, { childList: true, subtree: true });
  };

  win.addEventListener('beforeinstallprompt', (event) => {
    event.preventDefault();
    deferredPrompt = event;
    show();
  });
  win.addEventListener('appinstalled', () => {
    deferredPrompt = null;
    hide();
  });
}

export function startPwa({ production, win = globalThis.window, moduleUrl = import.meta.url } = {}) {
  if (!win) return false;
  const allowed = canRegisterServiceWorker({
    production,
    supported: Boolean(win.navigator && 'serviceWorker' in win.navigator),
    secureContext: win.isSecureContext,
    hostname: win.location?.hostname,
  });
  if (!allowed) return false;
  watchInstallPrompt(win);
  const register = () => {
    win.navigator.serviceWorker.register(serviceWorkerUrl(moduleUrl), { scope: '/' }).catch(() => {
      // Registration is an enhancement; the console works the same without it.
    });
  };
  if (win.document.readyState === 'complete') register();
  else win.addEventListener('load', register, { once: true });
  return true;
}
