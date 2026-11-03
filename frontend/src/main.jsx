import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';
import { startPwa } from './pwa.js';
import './index.css';
import './pwa.css';

createRoot(document.getElementById('root')).render(<App />);
startPwa({ production: import.meta.env.PROD });
