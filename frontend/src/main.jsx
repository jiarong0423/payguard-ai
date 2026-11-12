import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';
import { startPwa } from './pwa.js';
import './index.css';
import './pwa.css';
import './theme/modules.css';

createRoot(document.getElementById('root')).render(<App />);
// Wide-screen layout rules load right after the first render (see wide/index.js).
// Until the wide rules are in, the page body stays hidden on wide screens (no layout jump); shown either way when done.
const showWide = () => document.documentElement.classList.add('wide-ready');
import('./wide/index.js').then(showWide, showWide);
setTimeout(showWide, 3000);
startPwa({ production: import.meta.env.PROD });
