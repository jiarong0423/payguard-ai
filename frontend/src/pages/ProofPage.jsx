// (P5 2026-11-12) Console Proof page: the ledger of real Sandbox evidence sends and an in-browser check of the send 3 PDF.
// Display only. Every value comes from frontend/src/data/proof_ledger_v1.json, whose quotes tests/frontend_proof_page.mjs
// checks line by line against the evidence files. The only request is a same-origin GET of the committed PDF copy
// (frontend/public/evidence/); the SHA-256 is computed by the browser's Web Crypto. No API, no session, no outside service.
// Containers (.tg-ledger, .tg-log, .tg-source, .tg-legend) are styled by theme/components.css; ProofPage.css only lays out.
// (F 2026-11-12) Source lines and the legend from theme/sources.js; dates through theme/format.js. The check's four steps
// are drawn as pending before the first press, and each turns done as it finishes.
// (R5 2026-11-12, P0 designer) The check runs in a dark "vault" panel (one dark area on the whole site), its lines drawn in
// order; the result is a seal on paper (MATCH in green, MISMATCH in red), never small coloured text on the dark panel.
// Hashes show in groups of eight; each ledger row can open the recorded lines it quotes. Reviews: ext_review/review_STYLEREF.md
// sections 2-3, review_FULL.md (Proof).
// (vteam 2026-11-12, ui_mock/vteam/CONSENSUS.md sections 1 and 8) The whole check is the page's one focus area and the
// site's one dark surface (.tg-focus.tg-focus--bleed.tg-vault, full width); the ledger sits on .tg-grid-paper.
import { useRef, useState } from 'react';
import ledger from '../data/proof_ledger_v1.json';
import { SourceLegend, SourceLine } from '../theme/sources.js';
import { dateLabel } from '../theme/format.js';
import checkSvg from '../theme/icons/check-circle.svg?raw';
import xSvg from '../theme/icons/x-circle.svg?raw';
import fingerprintSvg from '../theme/icons/fingerprint.svg?raw';
import fileSvg from '../theme/icons/file-text.svg?raw';
import './ProofPage.css';

const ICONS = { check: checkSvg, x: xSvg, fingerprint: fingerprintSvg, file: fileSvg };
export function Icon({ name }) {
  return <span className="tg-icon pp-icon" aria-hidden="true" dangerouslySetInnerHTML={{ __html: ICONS[name] }} />;
}

const plainStatus = (value) => (/^[A-Z_]+$/u.test(value) ? value.toLowerCase().split('_').join(' ').replace(/^./u, (c) => c.toUpperCase()) : value);
const fileName = (path) => path.split('/').pop();
const toHex = (buffer) => [...new Uint8Array(buffer)].map((byte) => byte.toString(16).padStart(2, '0')).join('');
const clock = () => new Date().toLocaleTimeString('en-GB', { hour12: false });
// A hash in groups of eight characters. The groups are spans with a gap, so a copy still gives one unbroken string.
const groups = (value) => value.match(/.{1,8}/gu) || [];
function Hash({ value, testId }) {
  return <span className="tg-mono pp-hashgroups" data-testid={testId}>{groups(value).map((part, index) => <span key={index}>{part}</span>)}</span>;
}
const shortHash = (value) => `${value.slice(0, 8)} … ${value.slice(-6)}`;


function FileCheck({ check }) {
  if (!check) return <span className="tg-small" title="The receipt records no byte-for-byte file comparison">—</span>;
  return check.state === 'match'
    ? <span className="tg-done pp-check"><Icon name="check" />Match</span>
    : <span className="pp-muted">Not compared</span>;
}

// Progressive disclosure: the exact lines this row quotes, each with its file and line number (checked by
// tests/frontend_proof_page.mjs). Nothing is fetched; the lines are the committed quotes.
const QUOTED = [['date', 'Date'], ['where', 'Sent from'], ['debug_id', 'PayPal reference'], ['readback', 'Read-back'], ['file_check', 'File check']];
function RecordedLines({ send }) {
  const lines = QUOTED.filter(([field]) => send[field]?.value);
  return <details className="pp-raw" data-testid="proof-row-lines">
    <summary>Show the recorded lines</summary>
    <ul>{lines.map(([field, label]) => <li key={field} title={`${send.file}:${send[field].line}`}><span className="pp-raw__label">{label}</span> <span className="tg-mono">{send[field].value}</span> <span className="pp-raw__where">line {send[field].line}</span></li>)}</ul>
  </details>;
}

function Ledger() {
  const sends = ledger.sends;
  const withId = sends.filter((send) => send.debug_id).length;
  const matched = sends.filter((send) => send.file_check?.state === 'match').length;
  return <div className="tg-ledger pp-ledger tg-grid-paper" data-testid="proof-ledger">
    <p className="pp-caption" id="pp-ledger-caption">Every real PayPal Sandbox evidence send on file, one row each</p>
    <table className="tg-ledger__table" aria-describedby="pp-ledger-caption">
      <thead><tr><th scope="col">Date</th><th scope="col" className="pp-nowrap">Sent from</th><th scope="col" className="pp-nowrap" title="PayPal-Debug-Id, the reference PayPal returned for each send">PayPal reference</th><th scope="col">Read-back</th><th scope="col">File check</th><th scope="col">Evidence file</th></tr></thead>
      <tbody>{sends.map((send) => <tr key={send.id} id={`ledger-${send.id}`} data-testid="proof-ledger-row" className={send.id === ledger.verify.send_id ? 'is-selected' : undefined}>
        <td className="tg-ledger__date"><time dateTime={send.date.value}>{dateLabel(send.date.value)}</time></td>
        <td className="pp-nowrap">{send.basis === 'HOSTED DEMO' ? 'Hosted demo' : 'Local console'}</td>
        <td className="tg-ledger__ref">{send.debug_id ? <span className="tg-mono">{send.debug_id.value}</span> : <span className="tg-small" title="This send predates the recorded Debug-Id">—</span>}</td>
        <td className="tg-ledger__status pp-nowrap">{plainStatus(send.readback.value)}</td>
        <td><FileCheck check={send.file_check} /></td>
        <td className="pp-ledger__src"><SourceLine kind={send.basis} source={send.source_key} exact /><RecordedLines send={send} /></td>
      </tr>)}</tbody>
      <tfoot><tr className="tg-ledger__total"><td colSpan={6}>{sends.length} sends · {withId} with a PayPal reference · {matched} with the served file matched byte for byte · highlighted: the send checked above</td></tr></tfoot>
    </table>
  </div>;
}

// The browser check, written as a log: fetch, hash, compare, result. All four lines show as pending before the first press;
// each turns done (or risk) as its step finishes.
const PLAN = [
  { step: 'fetch', title: 'Fetch the file', note: 'From this site only.' },
  { step: 'hash', title: 'Compute SHA-256 in your browser', note: 'Web Crypto, crypto.subtle.digest' },
  { step: 'compare', title: 'Compare with the fingerprint recorded at send time', note: 'Recorded SHA-256, shown on the left' },
  { step: 'result', title: 'Result', note: 'MATCH or MISMATCH' },
];
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
      push({ step: 'fetch', state: 'is-done', title: `Fetched ${fileName(verify.pdf)}`, note: `${bytes.current.length.toLocaleString('en-US')} bytes, from this site; nothing else is contacted.` });
      const data = bytes.current.slice();
      if (tamper) {
        data[verify.tamper_byte] ^= 1;
        push({ step: 'tamper', state: 'is-risk', title: `Changed one byte (byte ${verify.tamper_byte})`, note: 'Only this copy in memory; the file itself is untouched.' });
      }
      const computed = toHex(await crypto.subtle.digest('SHA-256', data));
      push({ step: 'hash', state: 'is-done', title: 'Computed SHA-256 in your browser', note: 'Web Crypto, crypto.subtle.digest', ref: computed });
      const ok = computed === recorded;
      push({ step: 'compare', state: ok ? 'is-done' : 'is-risk', title: 'Compared with the fingerprint recorded at send time', note: row.label, ref: recorded });
      push({ step: 'result', state: ok ? 'is-done' : 'is-risk', title: ok ? 'Same file' : 'Different file', note: ok ? 'Every byte matches what was sent.' : 'The fingerprint no longer matches.', verdict: ok ? 'MATCH' : 'MISMATCH', computed });
      setResult({ ok, computed, tamper });
    } catch (error) {
      push({ step: 'error', state: 'is-risk', title: 'That did not go through. Nothing was sent anywhere.', note: `${error.message}. You can download the file and run: shasum -a 256 ${fileName(verify.pdf)}` });
    } finally {
      setBusy(false);
    }
  };

  return <section className="pp-verify tg-focus tg-focus--bleed tg-vault" id="verify" aria-labelledby="pp-verify-title" data-testid="proof-verify">
    <div className="pp-verify__head">
      <p className="tg-eyebrow">Check it yourself</p>
      <h3 id="pp-verify-title" className="tg-h3">Is the file PayPal holds the file TradeGlot sent?</h3>
      <p className="pp-verify__lede">{row.label} ({dateLabel(row.date.value)}): the console recorded the file's SHA-256 when it sent. {verify.pdf_note} Your browser can hash it and compare.</p>
      <dl className="pp-hash">
        <dt>Recorded at send time</dt><dd><Hash value={recorded} testId="proof-recorded-sha" /></dd>
        <dt>File</dt><dd><a className="tg-link" href={`${import.meta.env.BASE_URL}${verify.pdf}`} download><Icon name="file" />{fileName(verify.pdf)}</a> <span className="tg-small">{verify.served_bytes.value}</span></dd>
      </dl>
      <div className="tg-actions">
        <button type="button" className="tg-btn tg-btn--primary" data-testid="proof-verify-run" disabled={busy} onClick={() => run(false)}><Icon name="fingerprint" />Verify in your browser</button>
        {result && <button type="button" className="tg-btn tg-btn--secondary" data-testid="proof-verify-tamper" disabled={busy} onClick={() => run(!result.tamper)}>{result.tamper ? 'Check the original again' : 'Change one byte'}</button>}
      </div>
      {!result && <p className="pp-hint" data-testid="proof-tamper-hint">Verify first. You may then change one byte of the fetched copy, in memory only, and check again.</p>}
      <SourceLine kind={row.basis} source={row.source_key} exact />
    </div>
    <div className={`pp-verify__log pp-vault${entries.length ? ' is-run' : ''}`} aria-live="polite">
      <p className="pp-vault__head">{entries.length ? (result?.ok ? 'Checked. The file PayPal holds is the file that was sent.' : result ? 'Checked. This copy is not the file that was sent.' : 'Checking…') : 'Not checked yet. Nothing runs until you press Verify.'}</p>
      <ol className="tg-log" data-testid="proof-verify-log">{[...entries, ...PLAN.filter((plan) => !entries.some((entry) => entry.step === plan.step)).map((plan) => ({ ...plan, state: 'is-pending', pending: true }))].map((entry, index) => <li key={`${entry.step}-${index}-${entries.length}`} className={`tg-log__entry ${entry.state}`} data-step={entry.step} style={{ '--pp-i': index }}>
          {entry.pending ? <span className="tg-log__when pp-step-n" aria-label={`Step ${index + 1}, not run yet`}>Step {index + 1}</span> : <time className="tg-log__when">{entry.at}</time>}
          <div className="tg-log__body">
            <p className="tg-log__title">{entry.title}</p>
            <p className="tg-log__note">{entry.note}</p>
            {entry.ref && <p className="tg-log__ref">{entry.ref === recorded ? <Hash value={entry.ref} /> : <HashDiff value={entry.ref} against={recorded} />}</p>}
            {entry.verdict && <div className={`pp-seal ${entry.verdict === 'MATCH' ? 'pp-seal--ok' : 'pp-seal--risk'}`}>
              <span className={`tg-stamp ${entry.verdict === 'MATCH' ? 'tg-stamp--ok' : 'tg-stamp--risk'} pp-verdict is-new`} data-testid="proof-verdict"><Icon name={entry.verdict === 'MATCH' ? 'check' : 'x'} />{entry.verdict}</span>
              <span className="tg-mono pp-seal__hash">{shortHash(entry.computed)}</span>
            </div>}
          </div>
        </li>)}</ol>
      {result && !result.ok && <p className="pp-diff-note" data-testid="proof-diff">One changed byte changed the whole fingerprint (differing characters marked): this is what a different file looks like.</p>}
    </div>
  </section>;
}

function HashDiff({ value, against }) {
  return <span className="tg-mono pp-hashgroups">{groups(value).map((part, g) => <span key={g}>{[...part].map((char, k) => {
    const index = g * 8 + k;
    return char === against[index] ? char : <mark key={k} className="pp-diff">{char}</mark>;
  })}</span>)}</span>;
}

export default function ProofPage() {
  return <div className="pp" data-testid="proof-page">
    <Verify />
    <section aria-labelledby="pp-ledger-title" className="pp-section">
      <h3 id="pp-ledger-title" className="tg-h3">Sandbox evidence sends</h3>
      <Ledger />
    </section>
    <SourceLegend testId="proof-basis-legend" />
  </div>;
}
