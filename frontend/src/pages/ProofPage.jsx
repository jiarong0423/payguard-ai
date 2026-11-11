// (P5 2026-11-12) Console Proof page: the ledger of real Sandbox evidence sends and an in-browser check of the send 3 PDF.
// Display only. Every value comes from frontend/src/data/proof_ledger_v1.json, whose quotes tests/frontend_proof_page.mjs
// checks line by line against the evidence files. The only request is a same-origin GET of the committed PDF copy
// (frontend/public/evidence/); the SHA-256 is computed by the browser's Web Crypto. No API, no session, no outside service.
// Containers (.tg-ledger, .tg-log, .tg-source, .tg-legend) are styled by theme/components.css; ProofPage.css only lays out.
import { useRef, useState } from 'react';
import ledger from '../data/proof_ledger_v1.json';
import checkSvg from '../theme/icons/check-circle.svg?raw';
import xSvg from '../theme/icons/x-circle.svg?raw';
import fingerprintSvg from '../theme/icons/fingerprint.svg?raw';
import fileSvg from '../theme/icons/file-text.svg?raw';
import './ProofPage.css';

const ICONS = { check: checkSvg, x: xSvg, fingerprint: fingerprintSvg, file: fileSvg };
export function Icon({ name }) {
  return <span className="tg-icon pp-icon" aria-hidden="true" dangerouslySetInnerHTML={{ __html: ICONS[name] }} />;
}

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
export const plainDate = (iso) => {
  const [year, month, day] = iso.split('-').map(Number);
  return `${day} ${MONTHS[month - 1]} ${year}`;
};
const plainStatus = (value) => (/^[A-Z_]+$/u.test(value) ? value.toLowerCase().split('_').join(' ').replace(/^./u, (c) => c.toUpperCase()) : value);
const fileName = (path) => path.split('/').pop();
const toHex = (buffer) => [...new Uint8Array(buffer)].map((byte) => byte.toString(16).padStart(2, '0')).join('');
const clock = () => new Date().toLocaleTimeString('en-GB', { hour12: false });

// One line: LABEL · plain source; the full path and line sit in the title.
export function Source({ label, text, path }) {
  return <span className="tg-source" title={path}><span className="tg-source__label">{label}</span>· {text}</span>;
}

export function BasisLegend() {
  return <ul className="tg-legend" data-testid="proof-basis-legend" aria-label="What the source labels mean">
    {ledger.basis.map((item) => <li key={item.label}><b>{item.label}</b><span>{item.meaning}</span></li>)}
  </ul>;
}

function FileCheck({ check }) {
  if (!check) return <span className="tg-small" title="The receipt records no byte-for-byte file comparison">—</span>;
  return check.state === 'match'
    ? <span className="tg-pill tg-pill--ok">Match</span>
    : <span className="tg-pill">Not compared</span>;
}

function Ledger() {
  const sends = ledger.sends;
  const withId = sends.filter((send) => send.debug_id).length;
  const matched = sends.filter((send) => send.file_check?.state === 'match').length;
  return <div className="tg-ledger pp-ledger" data-testid="proof-ledger">
    <p className="pp-caption" id="pp-ledger-caption">Every real PayPal Sandbox evidence send on file, one row each</p>
    <table className="tg-ledger__table" aria-describedby="pp-ledger-caption">
      <thead><tr><th scope="col">Date</th><th scope="col" className="pp-nowrap">Sent from</th><th scope="col" className="pp-nowrap">PayPal-Debug-Id</th><th scope="col">Read-back</th><th scope="col">File check</th><th scope="col">Evidence file</th></tr></thead>
      <tbody>{sends.map((send) => <tr key={send.id} id={`ledger-${send.id}`} data-testid="proof-ledger-row" className={send.id === ledger.verify.send_id ? 'is-selected' : undefined}>
        <td className="tg-ledger__date"><time dateTime={send.date.value}>{plainDate(send.date.value)}</time></td>
        <td className="pp-nowrap">{send.basis === 'HOSTED DEMO' ? 'Hosted demo' : 'Local console'}</td>
        <td className="tg-ledger__ref">{send.debug_id ? <span className="tg-mono">{send.debug_id.value}</span> : <span className="tg-small" title="This send predates the recorded Debug-Id">—</span>}</td>
        <td className="tg-ledger__status pp-nowrap"><span className="tg-pill">{plainStatus(send.readback.value)}</span></td>
        <td><FileCheck check={send.file_check} /></td>
        <td className="pp-ledger__src"><Source label={send.basis} text={`${send.label} · line ${(send.debug_id || send.readback).line}`} path={`${send.file}:${(send.debug_id || send.readback).line}`} /></td>
      </tr>)}</tbody>
      <tfoot><tr className="tg-ledger__total"><td colSpan={6}>{sends.length} sends · {withId} with a PayPal-Debug-Id · {matched} with the served file matched byte for byte</td></tr></tfoot>
    </table>
  </div>;
}

// The browser check, written as a log: fetch, hash, compare, verdict. Each line appears as the step finishes.
function Verify() {
  const verify = ledger.verify;
  const recorded = verify.recorded_sha256.value;
  const row = ledger.sends.find((send) => send.id === verify.send_id);
  const bytes = useRef(null);
  const [entries, setEntries] = useState([]);
  const [result, setResult] = useState(null);
  const [busy, setBusy] = useState(false);

  const run = async (tamper) => {
    setBusy(true);
    setResult(null);
    const log = [];
    const push = (entry) => { log.push({ ...entry, at: clock() }); setEntries([...log]); };
    try {
      if (!bytes.current || !tamper) {
        const response = await fetch(`${import.meta.env.BASE_URL}${verify.pdf}`, { cache: 'no-store' });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        bytes.current = new Uint8Array(await response.arrayBuffer());
      }
      push({ state: 'is-done', title: `Fetched ${fileName(verify.pdf)}`, note: `${bytes.current.length.toLocaleString('en-US')} bytes, from this site; nothing else is contacted.` });
      const data = bytes.current.slice();
      if (tamper) {
        data[verify.tamper_byte] ^= 1;
        push({ state: 'is-risk', title: `Changed one byte (byte ${verify.tamper_byte})`, note: 'Only this copy in memory; the file itself is untouched.' });
      }
      const computed = toHex(await crypto.subtle.digest('SHA-256', data));
      push({ state: 'is-done', title: 'Computed SHA-256 in your browser', note: 'Web Crypto, crypto.subtle.digest', ref: computed });
      const ok = computed === recorded;
      push({ state: ok ? 'is-done' : 'is-risk', title: 'Compared with the fingerprint recorded at send time', note: row.label, ref: recorded, verdict: ok ? 'MATCH' : 'MISMATCH' });
      setResult({ ok, computed, tamper });
    } catch (error) {
      push({ state: 'is-risk', title: 'Could not read the file here', note: `${error.message}. Download it and run: shasum -a 256 ${fileName(verify.pdf)}` });
    } finally {
      setBusy(false);
    }
  };

  return <section className="pp-verify" aria-labelledby="pp-verify-title" data-testid="proof-verify">
    <div className="pp-verify__head">
      <p className="tg-eyebrow">Check it yourself</p>
      <h3 id="pp-verify-title" className="tg-h3">Is the file PayPal holds the file TradeGlot sent?</h3>
      <p className="pp-verify__lede">{row.label} ({plainDate(row.date.value)}): the console recorded the file's SHA-256 when it sent. {verify.pdf_note} Your browser can hash it and compare.</p>
      <dl className="pp-hash">
        <dt>Recorded at send time</dt><dd className="tg-mono" data-testid="proof-recorded-sha">{recorded}</dd>
        <dt>File</dt><dd><a className="tg-link" href={`${import.meta.env.BASE_URL}${verify.pdf}`} download><Icon name="file" />{fileName(verify.pdf)}</a> <span className="tg-small">{verify.served_bytes.value}</span></dd>
      </dl>
      <div className="tg-actions">
        <button type="button" className="tg-btn tg-btn--primary" data-testid="proof-verify-run" disabled={busy} onClick={() => run(false)}><Icon name="fingerprint" />Verify in your browser</button>
        <button type="button" className="tg-btn tg-btn--secondary" data-testid="proof-verify-tamper" disabled={busy || !result} onClick={() => run(!result?.tamper)}>{result?.tamper ? 'Check the original again' : 'Change one byte'}</button>
      </div>
      <Source label={row.basis} text={`${row.label} · line ${verify.recorded_sha256.line}`} path={`${verify.file}:${verify.recorded_sha256.line}`} />
    </div>
    <div className="pp-verify__log" aria-live="polite">
      {entries.length === 0
        ? <p className="tg-small pp-empty">The steps appear here: fetch, SHA-256, compare, result.</p>
        : <ol className="tg-log" data-testid="proof-verify-log">{entries.map((entry, index) => <li key={index} className={`tg-log__entry ${entry.state}`}>
          <time className="tg-log__when">{entry.at}</time>
          <div className="tg-log__body">
            <p className="tg-log__title">{entry.title}</p>
            <p className="tg-log__note">{entry.note}</p>
            {entry.ref && <p className="tg-log__ref tg-mono">{entry.ref === recorded ? entry.ref : <HashDiff value={entry.ref} against={recorded} />}</p>}
            {entry.verdict && <span className={`tg-stamp ${entry.verdict === 'MATCH' ? 'tg-stamp--ok' : 'tg-stamp--risk'} pp-verdict`} data-testid="proof-verdict"><Icon name={entry.verdict === 'MATCH' ? 'check' : 'x'} />{entry.verdict}</span>}
          </div>
        </li>)}</ol>}
      {result && !result.ok && <p className="pp-diff-note" data-testid="proof-diff">One changed byte changed the whole fingerprint (differing characters marked): this is what a different file looks like.</p>}
    </div>
  </section>;
}

function HashDiff({ value, against }) {
  return <>{[...value].map((char, index) => (char === against[index] ? char : <mark key={index} className="pp-diff">{char}</mark>))}</>;
}

export default function ProofPage() {
  return <div className="pp" data-testid="proof-page">
    <BasisLegend />
    <section aria-labelledby="pp-ledger-title" className="pp-section">
      <h3 id="pp-ledger-title" className="tg-h3">Sandbox evidence sends</h3>
      <Ledger />
    </section>
    <Verify />
  </div>;
}
