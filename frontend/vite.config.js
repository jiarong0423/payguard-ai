import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
import { fileURLToPath } from 'node:url';
import { existsSync } from 'node:fs';
import optionalBryntumTimeline from './src/optional/vitePlugin.js';

export default defineConfig({
  plugins: [react(), tailwindcss(), optionalBryntumTimeline({ root: fileURLToPath(new URL('.', import.meta.url)) })],
  server: {
    host: '127.0.0.1',
    port: 5173,
    strictPort: true,
    proxy: { '/api': { target: 'http://127.0.0.1:8000', changeOrigin: true } },
  },
  preview: { host: '127.0.0.1', port: 4173, strictPort: true },
  // Five pages: the seller console, the evidence page for reviewers, the AG Studio dispute evidence readiness
  // dashboard and the scenario work orders page (the console top bar links to these three and to the proof page).
  build: { rollupOptions: { input: {
    main: fileURLToPath(new URL('index.html', import.meta.url)),
    evidence: fileURLToPath(new URL('evidence.html', import.meta.url)),
    dashboard: fileURLToPath(new URL('dashboard.html', import.meta.url)),
    scenarios: fileURLToPath(new URL('scenarios.html', import.meta.url)),
    // Public proof page (optimise r24): static, built from committed JSON only, linked from the console top bar.
    // Added only when proof.html is present, because the hosted Dockerfile copies an explicit list of HTML files.
    ...(existsSync(fileURLToPath(new URL('proof.html', import.meta.url))) ? { proof: fileURLToPath(new URL('proof.html', import.meta.url)) } : {}),
  } } },
});
