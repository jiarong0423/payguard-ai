import React from 'react';
import { createRoot } from 'react-dom/client';
import BenchmarkCharts from './charts/BenchmarkCharts.jsx';
import { Short } from './theme/copy.jsx';
import './charts/evidence.css';

// The evidence page for judges and reviewers. It is not linked from the seller console: sellers never need it.
function EvidencePage() {
  return (
    <main className="evidence-page">
      <header className="evidence-header">
        <p className="evidence-eyebrow">TradeGlot · evidence</p>
        <h1>Drift control and model cost</h1>
        <p>How the guided gap filling keeps AI drift out of the dispute form and sends fewer sentences to the model. Every number below is read from the recorded benchmark file in the repository.</p>
      </header>
      <BenchmarkCharts />
      {/* (N2 C76) Phone: shorter line; the benchmark and the Channel3 receipts sit behind the info button. */}
      <p className="evidence-footer" data-testid="evidence-dashboard-link"><Short wide={<>See the same demo disputes, the benchmark and the Channel3 receipts in the <a href="/dashboard.html">AG Studio evidence dashboard</a>. Its evidence checker uses no AI.</>} phone={<>Same demo disputes in the <a href="/dashboard.html">AG Studio evidence dashboard</a>. Checker uses no AI.</>} more="The dashboard also has the benchmark and the Channel3 receipts." label="What else is there" /></p>
      <footer className="evidence-footer">Back to the <a href="/">merchant console</a>. Full method and limits: docs/evidence/GUIDE_BENCHMARK.md.</footer>
    </main>
  );
}

createRoot(document.getElementById('root')).render(<EvidencePage />);
