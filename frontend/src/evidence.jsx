import React from 'react';
import { createRoot } from 'react-dom/client';
import BenchmarkCharts from './charts/BenchmarkCharts.jsx';
import './charts/evidence.css';

// The evidence page for judges and reviewers. It is not linked from the seller console: sellers never need it.
function EvidencePage() {
  return (
    <main className="evidence-page">
      <header className="evidence-header">
        <p className="evidence-eyebrow">PayGuard AI · evidence</p>
        <h1>Drift control and model cost</h1>
        <p>How the guided gap filling keeps AI drift out of the dispute form and sends fewer sentences to the model. Every number below is read from the recorded benchmark file in the repository.</p>
      </header>
      <BenchmarkCharts />
      <p className="evidence-footer" data-testid="evidence-dashboard-link">See the same synthetic disputes, the benchmark and the Channel3 receipts in the <a href="/dashboard.html">AG Studio dispute evidence readiness dashboard</a>, with an evidence auditor that runs without a model.</p>
      <footer className="evidence-footer">Back to the <a href="/">merchant console</a>. Full method and limits: docs/evidence/GUIDE_BENCHMARK.md.</footer>
    </main>
  );
}

createRoot(document.getElementById('root')).render(<EvidencePage />);
