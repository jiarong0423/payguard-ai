import { lazy, Suspense, useEffect, useMemo, useRef, useState } from 'react';
import { apiRequest, retrySecondsLeft, waitText, withoutFixedWait } from './api.js';
import './GuideLive.css';

// Local stand-in with the props of C1's shared GapGrid ({ items, testIdPrefix }), built from the current GuideReplay pieces.
const PHONE_QUERY = '(max-width: 640px)';
const usePhone = () => {
  const [phone, setPhone] = useState(() => typeof window !== 'undefined' && window.matchMedia?.(PHONE_QUERY).matches);
  useEffect(() => {
    const query = window.matchMedia?.(PHONE_QUERY);
    if (!query) return undefined;
    const update = () => setPhone(query.matches);
    query.addEventListener('change', update);
    return () => query.removeEventListener('change', update);
  }, []);
  return phone;
};

function LiveGapGrid({ grid, Grid, items, testIdPrefix }) {
  const { gapGridTheme, StatusChip, SourceChip } = grid;
  const phone = usePhone();
  const columns = useMemo(() => [
    { field: 'label', headerName: 'Item', flex: 1.4, minWidth: 170, sortable: true },
    { field: 'status', headerName: 'Status', flex: 1.6, minWidth: 220, cellRenderer: ({ value }) => <StatusChip value={value} />, sortable: true },
    { field: 'source', headerName: 'Source', flex: 1, minWidth: 150, cellRenderer: ({ data }) => <SourceChip data={data} />, sortable: true },
  ], [StatusChip, SourceChip]);
  // Phones get stacked cards: three 150px+ columns do not fit 343px (review r1 P0.5).
  if (phone) return <ul className="guide-live-cards" data-testid={`${testIdPrefix}-grid-body`}>
    {items.map((item) => <li key={item.id} className="guide-live-card"><strong>{item.label}</strong><span><StatusChip value={item.status} /><SourceChip data={item} /></span></li>)}
  </ul>;
  return <div data-testid={`${testIdPrefix}-grid-body`}><Grid theme={gapGridTheme} rowData={items} columnDefs={columns} getRowId={({ data }) => data.id}
    domLayout="autoHeight" rowHeight={46} headerHeight={46} suppressCellFocus /></div>;
}

// The grid (grid/agGrid.jsx: module registration + AgGridReact) arrives with this lazy chunk, so AG Grid stays out of the entry chunk.
const GapGrid = lazy(() => Promise.all([import('./GuideReplay.jsx'), import('./grid/agGrid.jsx')])
  .then(([grid, ag]) => ({ default: (props) => <LiveGapGrid grid={grid} Grid={ag.AgGridReact} {...props} /> })));

const SITUATIONS = [['dispute', 'Dispute evidence'], ['velocity', 'Sales spike'], ['preflight', 'Policy pre-check']];
const MAX_TEXT = 400;
const FALLBACK_TEXT = {
  budget: 'model budget, rate limit or breaker',
  provider_error: 'model timeout or error',
  invalid_reply: 'model reply did not pass the strict check',
  late: 'model reply did not arrive within 30 seconds',
  no_items: 'model found no item in that sentence',
};
const KEPT_TEXT = {
  budget: 'Kept the quick answer: the model limit was reached.',
  provider_error: 'Kept the quick answer: the model was unavailable.',
  invalid_reply: 'Kept the quick answer: the model reply did not pass the strict check.',
  late: 'Kept the quick answer: the model did not answer within 30 seconds.',
  superseded: 'Kept the quick answer: a later entry came first.',
  no_items: 'Kept the quick answer: the model found no item in that sentence.',
};
const POLL_MS = 800;
const POLL_LIMIT_MS = 24000;

function chooserText(reply) {
  if (!reply) return '';
  if (reply.chooser === 'none') return 'Fixed rule';
  if (reply.chooser === 'keyword') return reply.state_changed ? 'Matched a word' : 'No word matched';
  if (reply.chooser === 'model') return reply.state_changed ? 'Gemini matched it; checked by rules' : 'Gemini found nothing to count';
  if (reply.chooser === 'form') return 'Form check';
  return `Word match (${FALLBACK_TEXT[reply.fallback_reason] || 'model unavailable'})`;
}

// Which items a reply moved, read from the gap table before and after (the reply itself names no item).
function changedLabels(before, after) {
  const was = Object.fromEntries((before || []).map((item) => [item.id, item.status]));
  return (after || []).filter((item) => item.id in was && was[item.id] !== item.status).map((item) => item.label);
}

// Badge at the top of a reply bubble (review r1 P1.12): who answered and what it filled. `ruled` are items the rule
// layer settled in the same turn, so a Gemini badge never claims them (r30 J3 #1).
function whoBadge(reply, before, after, ruled = []) {
  if (!reply || reply.chooser === 'form' || reply.chooser === 'none') return '';
  const who = reply.chooser === 'model' ? 'Gemini' : 'Rules';
  const moved = changedLabels(before, after).filter((label) => who === 'Rules' || !ruled.includes(label));
  return `${who} → ${moved.length ? moved.join(', ') : 'nothing counted'}`;
}

// (r30 J3 #1) The hybrid funnel under each reply, in one plain line: model calls this turn and what the rules did.
// A model step counts as 1 from the moment it is started ("analysing"), whatever its outcome; with no step it is 0.
// The step is the backend's single governed step (governed_model_rows: one call, one identical resend only when the
// first reply fails the strict check), and a budget refusal can come before or after its first call.
const MODEL_CALLS_TEXT = {
  analysing: '1 (Gemini, running)',
  replaced: '1 (Gemini, checked by rules)',
  kept: '1 (Gemini, answer not used)',
  budget: 'at most 1 (model limit reached)',
};
// Rules filled = marked present by the rule layer from the seller's words (auto_confirmed) or by a form entry that
// passed the rule check; rules marked = a keyword match that moved an item's status without filling it.
// (r31 J3) Gemini marked = items the accepted model answer moved, with the status it set, so a Gemini turn that
// marked ship date "Mentioned, not confirmed" no longer reads "Nothing filled" under "Gemini → ship date".
function funnelLine(model, filled, marked = [], filledBy = 'Rules filled', modelMarked = []) {
  const rules = [filled.length ? `${filledBy}: ${filled.join(', ')}` : '', marked.length ? `Rules marked: ${marked.join(', ')}` : '',
    modelMarked.length ? `Gemini marked: ${modelMarked.join(', ')}` : ''].filter(Boolean);
  return `Model calls this turn: ${model ? MODEL_CALLS_TEXT[model] : '0'} · ${rules.length ? rules.join(' · ') : 'Nothing filled'}`;
}
// (r32 J1) While the Gemini step runs, the reply bubble shows a neutral running state instead of the quick word-match
// answer: "No word matched" for 5 to 10 s before Gemini's answer replaced it read as a miss on camera. The quick
// answer is held back and shown only when the model answer is not used (kept, limit, late or superseded); the funnel
// line counts the call from the start ("1 (Gemini, running)"), and the gap table is the backend's, unchanged.
const RUNNING_TEXT = 'Checking with Gemini…';
const RUNNING_NOTE = 'Gemini is reading this sentence. If its answer is not used, the word-match answer is shown here.';
function runningRow(funnel) {
  return { text: RUNNING_TEXT, template: undefined, meta: '', badge: '', dropped: '', analysing: true, funnel };
}
// (r31 J3) The status an item was moved to, in the words of the gap table (GuideReplay STATUS_TEXT), short form.
const MARKED_TEXT = {
  PARTIAL: 'not confirmed',
  UNCLEAR: 'unclear',
  CONFLICTING: 'two different answers',
  STRUCTURALLY_PRESENT: 'filled in, not checked',
  MISSING: 'not filled in',
};
// Items the model answer moved (same rule as the Gemini badge: never an item the rule layer settled this turn).
function modelMarks(before, after, ruled = []) {
  const was = Object.fromEntries((before || []).map((item) => [item.id, item.status]));
  return (after || []).filter((item) => item.id in was && was[item.id] !== item.status && !ruled.includes(item.label))
    .map((item) => (MARKED_TEXT[item.status] ? `${item.label} (${MARKED_TEXT[item.status]})` : item.label));
}
const autoLabels = (view) => (view?.auto_confirmed || []).map((id) => view.items.find((item) => item.id === id)?.label).filter(Boolean);

function droppedText(reply, labels) {
  if (!reply?.dropped?.length) return '';
  return reply.dropped.map((row) => `${labels[row.item] || row.item}: ${row.reason === 'inferred' ? 'only implied' : 'said by the buyer'}`).join(' · ');
}

const STAGE_HEADINGS = {
  funnel: ['Quick questions', 'Pick an answer for each item.'],
  echo: ['Check what we read', 'Read from what you wrote. Confirm or change.'],
  fill: ['Still missing', 'Type it in the message box, or pick an answer.'],
  done: ['Every item has an entry', 'Check each one before you download.'],
};
const NOT_SURE = 'not_sure';
const SKIP = 'skip';

function RoundField({ item, value, onChange, disabled }) {
  const form = item.form;
  const fieldId = `guide-live-field-${item.id}`;
  const notSure = value === NOT_SURE;
  const hasNotSureOption = form.options.some((option) => option.value === NOT_SURE);
  return <div className="guide-live-field" data-testid={`guide-live-form-${item.id}`}>
    <label htmlFor={fieldId}>{item.label}</label>
    {form.kind === 'choice'
      ? <select id={fieldId} value={value} disabled={disabled} onChange={(event) => onChange(event.target.value)}>
        <option value="">Choose one</option>
        {form.options.map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}
      </select>
      : <input id={fieldId} type={form.kind === 'date' ? 'date' : 'text'} value={notSure ? '' : value} disabled={disabled || notSure}
        maxLength={form.kind === 'date' ? 10 : 60} placeholder={form.placeholder || ''} autoComplete="off" spellCheck={false}
        onChange={(event) => onChange(event.target.value)} />}
    {!hasNotSureOption && <label className="guide-live-notsure"><input type="checkbox" checked={notSure} disabled={disabled}
      onChange={(event) => onChange(event.target.checked ? NOT_SURE : '')} />Not sure</label>}
  </div>;
}

// The one summary at the end: what came from the seller's words, confirmed once, or items picked to change.
function ReviewPanel({ view, disabled, onReview }) {
  const [change, setChange] = useState([]);
  const label = (id) => view.items.find((item) => item.id === id)?.label || id;
  const toggle = (id) => setChange((current) => (current.includes(id) ? current.filter((item) => item !== id) : [...current, id]));
  return <div className="guide-live-forms" data-testid="guide-live-review" data-stage="review">
    <p className="guide-live-subtraction" data-testid="guide-live-subtraction">{view.subtraction.text}</p>
    <strong>Check once before you download</strong>
    <small>These came from what you wrote. Confirm them together, or tick the ones to change.</small>
    <ul className="guide-live-review-list">
      {view.review.map((row) => <li key={row.item}>
        <label className="guide-live-review-row"><input type="checkbox" data-testid={`guide-live-review-change-${row.item}`} checked={change.includes(row.item)}
          disabled={disabled} onChange={() => toggle(row.item)} />
          <span>{label(row.item)}: <strong>{row.value}</strong></span></label>
      </li>)}
    </ul>
    <div className="guide-live-round-actions">
      {change.length
        ? <button type="button" className="guide-live-primary" data-testid="guide-live-review-change" disabled={disabled} onClick={() => onReview({ change })}>Change {change.length}</button>
        : <button type="button" className="guide-live-primary" data-testid="guide-live-review-confirm" disabled={disabled} onClick={() => onReview({ confirm: true })}>Confirm summary</button>}
    </div>
  </div>;
}

// One round: the subtraction line, up to three asked items with their fixed inputs, one Save (or Confirm).
function RoundPanel({ view, disabled, onSave, onReview }) {
  const asked = view.asked.map((id) => view.items.find((item) => item.id === id)).filter(Boolean);
  const [values, setValues] = useState(() => Object.fromEntries(asked.map((item) => [item.id, view.prefill[item.id] || ''])));
  const [heading, hint] = STAGE_HEADINGS[view.stage] || STAGE_HEADINGS.funnel;
  const summary = view.stage !== 'review' && view.review.length > 0;  // the last round carries the summary
  const save = (event) => {
    event.preventDefault();
    if (disabled) return;
    onSave(asked.map((item) => ({ item: item.id, value: values[item.id] || SKIP })), summary);
  };
  const echo = view.stage === 'echo';
  const changed = echo && asked.some((item) => values[item.id] !== view.prefill[item.id]);
  return <form className="guide-live-forms" data-testid="guide-live-round" data-stage={view.stage} onSubmit={save}>
    <p className="guide-live-subtraction" data-testid="guide-live-subtraction">{view.subtraction.text}</p>
    {view.auto_confirmed.length > 0 && <p className="guide-live-auto" data-testid="guide-live-auto">
      Taken from what you wrote: {view.auto_confirmed.map((id) => view.items.find((item) => item.id === id)?.label).filter(Boolean).join(', ')}. You can change any item before you download.</p>}
    <strong>{heading}</strong>
    <small>{hint}</small>
    {asked.map((item) => <RoundField key={item.id} item={item} value={values[item.id] || ''} disabled={disabled}
      onChange={(value) => setValues((current) => ({ ...current, [item.id]: value }))} />)}
    {summary && <div className="guide-live-summary" data-testid="guide-live-summary">
      <small>Taken from what you wrote. Saving also confirms these, or reopen one to answer it again.</small>
      <ul className="guide-live-review-list">{view.review.map((row) => <li key={row.item} className="guide-live-review-row">
        <span>{view.items.find((item) => item.id === row.item)?.label || row.item}: <strong>{row.value}</strong></span>
        <button type="button" className="guide-live-secondary" data-testid={`guide-live-summary-change-${row.item}`} disabled={disabled}
          onClick={() => onReview({ change: [row.item] })}>Change</button></li>)}</ul>
    </div>}
    {asked.length > 0 && <div className="guide-live-round-actions">
      <button type="submit" className="guide-live-primary" data-testid="guide-live-save" aria-disabled={disabled || undefined}>
        {summary ? 'Save and confirm summary' : echo && !changed ? 'Confirm' : 'Save'}</button>
      {echo && <small>{changed ? 'Saving your changed values.' : 'Confirm keeps these values; change any field first if it is wrong.'}</small>}
      {!echo && <small>Empty fields are skipped and asked again later in your own words.</small>}
    </div>}
  </form>;
}

const ROUTE_TEXT = {
  catalogue_match: 'Matches the Channel3 catalogue',
  live_catalogue_match: 'Matches a live Channel3 search',
  digital_word: 'Digital goods word',
  service_word: 'A service: the dispute items do not cover services yet; describe it in your own words.',
  filtered_conflict: 'Similar products were found, but none has your size or model. Pick physical or digital below.',
  no_close_match: 'No close match. Pick physical or digital below.',
  nothing_to_match: 'Nothing to match after removing personal details.',
};

function RouteResult({ route }) {
  const routed = route.route === 'physical' || route.route === 'digital';
  return <div className="guide-route-result" data-testid="guide-route-result" data-route={route.route} aria-live="polite">
    <p><strong>{routed ? `Routed to ${route.route} goods` : route.route === 'service' ? 'Not routed' : 'Not routed yet'}</strong>
      {' · '}{ROUTE_TEXT[route.reason]}{route.matched_word ? ` ("${route.matched_word}")` : ''}</p>
    {route.matches.length > 0 && <ul className="guide-route-matches">{route.matches.map((match) => <li key={match.product_id}>
      <span className={`guide-route-type guide-route-type-${match.match_type}`}>{match.match_type === 'exact' ? 'Exact match' : 'Close match'}</span>{' '}
      {match.title}{match.category ? ` · ${match.category}` : ''} <span className="guide-route-score">{Math.round(match.score * 100)}% fuzzy{match.exact_words.length ? ` · exact words: ${match.exact_words.join(', ')}` : ''}</span></li>)}</ul>}
    {route.filtered_out > 0 && <p className="guide-route-note" data-testid="guide-route-filtered">Filter removed {route.filtered_out} similar product{route.filtered_out === 1 ? '' : 's'} with a different size or model, or fewer exact words.</p>}
    {routed && <p className="guide-route-items">Items this case needs: {route.items.join(', ')}</p>}
    <p className="guide-route-note">Fuzzy search finds candidates, then a precise filter keeps only the best fit. Decided by code, not by AI. You can change the goods group below.</p>
  </div>;
}

// One guide per situation (owner 2026-11-02): each step mounts its own, the backend keeps each apart and the model
// gets that situation's own prompt, so one situation never clears, fills or steers another.
// A 401 goes to the console's own "Demo session expired + Reconnect" banner (attack r21 desktop #10).
const SESSION_EXPIRED_TEXT = 'The demo session expired. Select Reconnect at the top of the page to start a new one.';
// Plain words when a request never reached TradeGlot (attack r22: the offline text said "confirm that the API is
// running"). Shared with the console banner and the country panel.
export const OFFLINE_TEXT = 'TradeGlot could not be reached. Check your internet connection, then try again.';
export const plainFailureMessage = (failure, fallback = 'The request failed. Try again.') => (failure?.code === 'backend_unavailable' ? OFFLINE_TEXT : failure?.message || fallback);
// (attack r23) A 429 or 503 with Retry-After: the server's fixed wait sentence makes room for the live countdown.
export const waitFailureMessage = (failure, fallback) => (failure?.retryAt ? withoutFixedWait(plainFailureMessage(failure, fallback)) : plainFailureMessage(failure, fallback));
// (attack r23) Re-renders about twice a second until `until` (epoch ms) has passed, and returns the current time, so
// "Try again in N seconds" counts down. Shared with the console and the country panel.
export function useWaitClock(until) {
  const [now, setNow] = useState(() => Date.now());
  useEffect(() => {
    setNow(Date.now());
    if (!until || until <= Date.now()) return undefined;
    const timer = window.setInterval(() => { const at = Date.now(); setNow(at); if (at >= until) window.clearInterval(timer); }, 500);
    return () => window.clearInterval(timer);
  }, [until]);
  return now;
}
// The countdown line: "Try again in N seconds." while waiting, then "You can try again now."
export const WaitLine = ({ until, now, testId }) => (until ? <span className="wait-line" data-testid={testId} aria-live="off">{' '}{until > now ? waitText(Math.max(1, Math.ceil((until - now) / 1000))) : 'You can try again now.'}</span> : null);

export default function GuideLive({ session, Disclosure, Badge, request, scenario, onSessionExpired, onOpenItems, onChooser }) {
  const [open, setOpen] = useState(false);
  const [goods, setGoods] = useState('physical');
  const [view, setView] = useState(null);
  const [log, setLog] = useState([]);
  const [text, setText] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  // (attack r23) Until when a 429/503 Retry-After holds this guide's buttons (epoch ms; 0 = no wait).
  const [waitUntil, setWaitUntil] = useState(0);
  const now = useWaitClock(waitUntil);
  const waiting = waitUntil > now;
  const holdFor = (failure) => setWaitUntil(retrySecondsLeft(failure) ? failure.retryAt : 0);
  const [routeText, setRouteText] = useState('');
  const [route, setRoute] = useState(null);
  const logRef = useRef(null);
  const inputRef = useRef(null);
  const routeInputRef = useRef(null);
  const nextId = useRef(0);
  const pendingRef = useRef(null); // { turn, rowId } of the one turn whose model step is still running
  const jumpRef = useRef(false); // the "Start here" box asked for this guide, until its form is on screen
  const title = SITUATIONS.find(([id]) => id === scenario)?.[1] || 'Guide';
  const stepNumber = { preflight: '01', velocity: '02', dispute: '03' }[scenario];
  const sectionId = `guide-live-${scenario}`;

  const labels = useMemo(() => Object.fromEntries((view?.items || []).map((item) => [item.id, item.label])), [view]);

  useEffect(() => {
    if (!open || !session || view) return;
    let live = true;
    apiRequest(`/guide/state?scenario=${scenario}`, { session }).then((result) => {
      if (!live) return;
      setView(result);
      if (result.started && result.reply) setLog([{ id: nextId.current++, who: 'payguard', text: result.reply.text, template: result.reply.template, meta: 'Resumed this session' }]);
    }).catch(() => {});
    return () => { live = false; };
  }, [open, session, view]);

  // (r33 M3) After a turn the newest reply's top (its badge) stays in view: scrolling only to the bottom pushed the
  // "Gemini → ship date" badge out of the box on a phone, where a long reply is taller than the log. A reply that fits
  // is shown whole (bottom); a taller one is scrolled to its own top.
  useEffect(() => {
    const box = logRef.current;
    if (!box?.scrollTo) return;
    const newest = box.lastElementChild;
    if (!newest) return;
    const pad = 8;
    const newestTop = box.scrollTop + newest.getBoundingClientRect().top - box.getBoundingClientRect().top - pad;
    box.scrollTo({ top: Math.max(0, Math.min(newestTop, box.scrollHeight - box.clientHeight)) });
  }, [log]);

  // "Start here" jump for this situation: open its guide, start it if it has not started (a running one is kept as it
  // is), and bring its form on screen. Other situations' guides are separate and never touched.
  useEffect(() => {
    if (!request || request.scenario !== scenario) return;
    jumpRef.current = true;
    setOpen(true);
  }, [request, scenario]);
  useEffect(() => {
    if (!jumpRef.current || !open || !view || busy) return;
    jumpRef.current = false;
    // Scroll once now and once after the step's lazy parts have laid out (on a phone they push the guide down by
    // hundreds of pixels; review r8), then move focus to the guide's own heading so keyboard and screen-reader users
    // land on it too.
    const reveal = () => {
      const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      const go = (behavior) => document.getElementById(sectionId)?.scrollIntoView({ behavior, block: 'start' });
      window.requestAnimationFrame(() => go(reducedMotion ? 'auto' : 'smooth'));
      window.setTimeout(() => {
        go('auto');
        document.getElementById(`${sectionId}-trigger`)?.focus({ preventScroll: true });
      }, 450);
    };
    if (view.started) reveal();
    else start().then(reveal);
  }, [open, view, busy, request]); // eslint-disable-line react-hooks/exhaustive-deps -- request: a second click while the guide is already open

  const push = (who, entry) => {
    const id = nextId.current++;
    setLog((rows) => [...rows.slice(-39), { id, who, ...entry }]);
    return id;
  };
  const patchRow = (id, change) => setLog((rows) => rows.map((row) => (row.id === id ? { ...row, ...change } : row)));

  // Resolve the pending turn from a response: replaced -> show the model's fixed answer; kept -> neutral note.
  const settle = (result) => {
    const pending = pendingRef.current;
    if (!pending) return;
    const analysis = result.analysis;
    if (analysis && analysis.turn === pending.turn && analysis.status === 'analysing') return;
    pendingRef.current = null;
    if (analysis && analysis.turn === pending.turn && analysis.status === 'replaced' && result.reply.chooser === 'model') {
      patchRow(pending.rowId, { text: result.reply.text, template: result.reply.template, analysing: false,
        meta: `${chooserText(result.reply)} · used instead of the quick answer`, badge: whoBadge(result.reply, pending.before, result.items, pending.filled),
        dropped: droppedText(result.reply, labels),
        funnel: funnelLine('replaced', pending.filled, [], 'Rules filled', modelMarks(pending.before, result.items, pending.filled)) });
    } else {
      const reason = analysis && analysis.turn === pending.turn && analysis.status === 'kept' ? analysis.reason : 'superseded';
      patchRow(pending.rowId, { ...pending.quick, analysing: false, note: KEPT_TEXT[reason] || KEPT_TEXT.provider_error,
        funnel: funnelLine(reason === 'budget' ? 'budget' : 'kept', pending.filled, pending.marked) });
    }
  };

  useEffect(() => {
    if (!session || !pendingRef.current) return undefined;
    let live = true;
    const startedAt = Date.now();
    const timer = setInterval(() => {
      if (!pendingRef.current) { clearInterval(timer); return; }
      if (Date.now() - startedAt > POLL_LIMIT_MS) {
        clearInterval(timer);
        const { rowId, filled, marked, quick } = pendingRef.current;
        patchRow(rowId, { ...quick, analysing: false, note: KEPT_TEXT.late, funnel: funnelLine('kept', filled, marked) });
        pendingRef.current = null;
        return;
      }
      // Poll this guide's own situation: without it the backend answers with the guide started last (review r8).
      apiRequest(`/guide/state?scenario=${scenario}`, { session }).then((result) => {
        if (!live || !pendingRef.current) return;
        if (result.analysis?.status !== 'analysing' || result.analysis?.turn !== pendingRef.current.turn) {
          setView(result);
          settle(result);
          clearInterval(timer);
        }
      }).catch(() => {});
    }, POLL_MS);
    return () => { live = false; clearInterval(timer); };
  }, [session, log.length]); // eslint-disable-line react-hooks/exhaustive-deps

  // Fuzzy case routing: code matches what the seller sold to a goods group, which picks the dispute items.
  // A route belongs to the text it was found for: any edit clears it until the seller asks again.
  const editRouteText = (value) => { setRouteText(value); setRoute(null); };
  const findRoute = async () => {
    if (!session || busy || !routeText.trim() || Date.now() < waitUntil) return;
    setBusy(true);
    setError('');
    setWaitUntil(0);
    try {
      const result = await apiRequest('/cases/route', { method: 'POST', body: { text: routeText }, session });
      setRoute(result);
      if (result.route === 'physical' || result.route === 'digital') setGoods(result.route);
    } catch (failure) {
      holdFor(failure);
      setError(failure.status === 401 ? SESSION_EXPIRED_TEXT : waitFailureMessage(failure));
      if (failure.status === 401) onSessionExpired?.(failure, session);
    } finally {
      setBusy(false);
      routeInputRef.current?.focus({ preventScroll: true });
    }
  };

  const call = async (path, body) => {
    if (!session || busy || Date.now() < waitUntil) return null;
    setBusy(true);
    setError('');
    setWaitUntil(0);
    try {
      // Every call names this guide's situation; the backend keeps one guide per situation.
      const result = await apiRequest(path, { method: 'POST', body: path === '/guide/start' ? body : { ...body, scenario }, session });
      setView(result);
      settle(result);
      return result;
    } catch (failure) {
      holdFor(failure);
      setError(failure.status === 401 ? SESSION_EXPIRED_TEXT : waitFailureMessage(failure));
      if (failure.status === 401) onSessionExpired?.(failure, session);
      return null;
    } finally {
      setBusy(false);
    }
  };

  const start = async () => {
    const result = await call('/guide/start', { scenario, goods_type: scenario === 'dispute' ? goods : null });
    if (result) {
      setLog([]);
      push('payguard', { text: result.reply.text, template: result.reply.template, meta: 'New guide started', funnel: funnelLine(null, []) });
    }
  };

  const send = async (event) => {
    event.preventDefault();
    const message = text.trim();
    if (!message || busy || waiting) return;
    const before = view?.items;
    // The text stays in the box until the turn is accepted, and the bubble reads "Sending" until then; a failed turn
    // (413, offline, 401, 429) removes the bubble and keeps the text to retry (attack r21 desktop #9).
    const sentId = push('seller', { text: message, meta: 'Sending…' });
    const result = await call('/guide/turn', { text: message });
    // Keep the keyboard on the message box (it stays readOnly, not disabled, while the turn runs).
    inputRef.current?.focus({ preventScroll: true });
    if (!result) { setLog((rows) => rows.filter((row) => row.id !== sentId)); return; }
    patchRow(sentId, { meta: '' });
    setText((current) => (current.trim() === message ? '' : current));
    const analysing = result.analysis?.status === 'analysing';
    // The rule layer acts before any model step, so its part of the funnel line is known now and stays as it is.
    const filled = autoLabels(result);
    const marked = changedLabels(before, result.items).filter((label) => !filled.includes(label));
    // (r32 J1) The quick answer; while Gemini runs it is held back and shown only if the model answer is not used.
    const quick = { text: result.reply.text, template: result.reply.template, meta: chooserText(result.reply),
      badge: analysing ? '' : whoBadge(result.reply, before, result.items), dropped: droppedText(result.reply, labels) };
    const rowId = push('payguard', analysing ? runningRow(funnelLine('analysing', filled, marked))
      : { ...quick, analysing: false, funnel: funnelLine(null, filled, marked) });
    pendingRef.current = analysing ? { turn: result.analysis.turn, rowId, before, filled, marked, quick } : null;
  };

  const saveRound = async (fields, confirmReview = false) => {
    const result = await call('/guide/form', confirmReview ? { fields, confirm_review: true } : { fields });
    if (!result) return;
    const lines = result.form_results.map((row) => `${labels[row.item] || row.item}: ${row.valid ? 'passed the rule check, taken' : row.deferred ? 'not sure, asked later in your own words' : 'did not pass the rule check'}`);
    push('form', { text: lines.join(' · ') });
    const taken = result.form_results.filter((row) => row.valid).map((row) => labels[row.item] || row.item);
    push('payguard', { text: result.reply.text, template: result.reply.template, meta: chooserText(result.reply), funnel: funnelLine(null, taken, [], 'Form check filled') });
  };

  const review = async (body) => {
    const result = await call('/guide/review', body);
    if (!result) return;
    push('form', { text: body.confirm ? 'Summary confirmed.' : `Reopened: ${body.change.map((id) => labels[id] || id).join(', ')}` });
    push('payguard', { text: result.reply.text, template: result.reply.template, meta: chooserText(result.reply), funnel: funnelLine(null, []) });
  };

  const started = Boolean(view?.started);
  // (r33 M4) Items the guide still needs (same rule as the backend's open_items: applicable and not structurally
  // present), reported to the page so Step 3's draft can say they are not part of it. 0 until the guide has started.
  const openCount = started ? (view.items || []).filter((item) => item.status !== 'STRUCTURALLY_PRESENT' && item.status !== 'NOT_APPLICABLE').length : 0;
  useEffect(() => { onOpenItems?.(openCount); }, [openCount]); // eslint-disable-line react-hooks/exhaustive-deps -- onOpenItems: a setState from the page
  useEffect(() => () => onOpenItems?.(0), []); // eslint-disable-line react-hooks/exhaustive-deps -- a remounted guide (new session) starts at 0
  const modeBadge = view?.chooser_mode === 'gemini' ? <Badge tone="muted">Rules + Gemini</Badge> : <Badge tone="muted">Rules only</Badge>;
  // (r34 #1) The same chooser status the badge above reads goes to the page, so the hosted "Why?" panel says what
  // this guide really does instead of a fixed "Gemini: Off".
  useEffect(() => {
    if (view?.chooser_mode) onChooser?.({ chooser_mode: view.chooser_mode, model_requested: view.model_requested === true });
  }, [view?.chooser_mode, view?.model_requested]); // eslint-disable-line react-hooks/exhaustive-deps -- onChooser: a setState from the page

  return <Disclosure id={sectionId} title={`Step ${stepNumber} guide: ${title}`} subtitle="Describe it in your own words" icon="layers"
    open={open} onToggle={setOpen} testId={`optional-toggle-guide-live-${scenario}`}>
    {open ? <section className="guide-live" data-testid={`guide-live-${scenario}`} data-scenario={scenario} aria-label={`Guided gap filling, live: ${title}`}>
      <p className="guide-live-intro">Type as a seller. TradeGlot shows which details are still missing.</p>
      <div className="guide-live-controls">
        {scenario === 'dispute' && <form className="guide-route" data-testid="guide-route" onSubmit={(event) => { event.preventDefault(); findRoute(); }}>
          <label>What did you sell?
            <input ref={routeInputRef} data-testid="guide-route-input" type="search" maxLength={200} value={routeText} readOnly={busy} placeholder="e.g. wireless headphones, ebook" onChange={(event) => editRouteText(event.target.value)} />
          </label>
          <button type="submit" className="guide-live-secondary" data-testid="guide-route-find" disabled={!session || !routeText.trim()} aria-disabled={busy || waiting || undefined} aria-busy={busy}>Find the route</button>
        </form>}
        {scenario === 'dispute' && route && <RouteResult route={route} />}
        {scenario === 'dispute' && <label>Goods
          <select data-testid="guide-live-goods" value={goods} disabled={busy} onChange={(event) => setGoods(event.target.value)}>
            <option value="physical">Physical</option>
            <option value="digital">Digital</option>
          </select>
        </label>}
        <button type="button" className={started ? 'guide-live-secondary' : 'guide-live-primary'} data-testid="guide-live-start" disabled={!session} aria-disabled={busy || waiting || undefined} aria-busy={busy} onClick={() => { if (!busy && !waiting) start(); }}>{started ? 'Restart guide' : 'Start guide'}</button>
        <span className="guide-live-mode" data-testid="guide-live-mode">{view ? modeBadge : null}</span>
      </div>
      {error && <p className="guide-live-error" role="alert">{error}<WaitLine until={waitUntil} now={now} testId="guide-live-wait" /></p>}
      {started && <div className="guide-live-layout">
        <div className="guide-live-chat">
          <ol className="guide-live-log" ref={logRef} role="log" aria-live="polite" data-testid="guide-live-log">
            {log.map((row) => <li key={row.id} className={`guide-live-msg guide-live-msg-${row.who}`}>
              <span className="guide-live-tag">{row.who === 'seller' ? 'You' : row.who === 'form' ? 'Form' : 'TradeGlot'}</span>
              {/* (r34 #12) First line of the reply: on a phone the line under a long reply fell below the log box. */}
              {row.funnel && <small className="guide-live-funnel" data-testid="guide-live-funnel">{row.funnel}</small>}
              {row.badge && <span className="guide-live-who" data-testid="guide-live-who">{row.badge}</span>}
              <p className={row.analysing ? 'guide-live-running' : undefined} data-testid={row.analysing ? 'guide-live-running' : undefined}>{row.text}</p>
              {row.dropped && <small className="guide-live-dropped"><span className="guide-live-chip">Not counted</span>{row.dropped}</small>}
              {/* The fixed template id is kept for tests and support, not shown to the seller (review r8). */}
              {row.meta && <small data-template={row.template || undefined}>{row.meta}</small>}
              {row.analysing && <small className="guide-live-analysing" role="status" data-testid="guide-live-analysing"><span className="guide-live-dot" aria-hidden="true" />{RUNNING_NOTE}</small>}
              {row.note && <small className="guide-live-note" data-testid="guide-live-note">{row.note}</small>}
            </li>)}
          </ol>
          <form className="guide-live-input" onSubmit={send}>
            {/* One guide per step: the id carries the scenario so each label points at its own box (click-all #4). */}
            <label htmlFor={`guide-live-text-${scenario}`} className="guide-live-sr">Message as the seller</label>
            <input ref={inputRef} id={`guide-live-text-${scenario}`} data-testid="guide-live-text" value={text} maxLength={MAX_TEXT} readOnly={busy} aria-busy={busy || undefined} autoComplete="off"
              placeholder="e.g. I shipped it last Monday with UPS" onChange={(event) => setText(event.target.value)} />
            <button type="submit" className="guide-live-primary" data-testid="guide-live-send" disabled={!busy && !waiting && !text.trim()} aria-disabled={busy || waiting || undefined} aria-busy={busy}>Send</button>
          </form>
          <small className="guide-live-count">{text.length}/{MAX_TEXT} · English · turn {view.turns_used} of {view.turns_limit}</small>
        </div>
        <div className="guide-live-side">
          <div className="guide-live-grid" data-testid="guide-live-grid">
            <Suspense fallback={<p className="guide-live-label">Loading the gap table.</p>}><GapGrid items={view.items} testIdPrefix="guide-live" /></Suspense>
          </div>
          {view.stage === 'review'
            ? <ReviewPanel key={`review-${view.rounds_used}`} view={view} disabled={busy} onReview={review} />
            : <RoundPanel key={`${view.rounds_used}-${view.stage}-${view.asked.join(',')}-${Object.entries(view.prefill).join(';')}`}
              view={view} disabled={busy} onSave={saveRound} onReview={review} />}
        </div>
      </div>}
      {/* (r30 J4 #6c) Kept, but collapsed at the very end of the panel, out of the main reading path. */}
      <details className="technical-details guide-live-technical" data-testid="guide-live-technical"><summary>Technical details</summary><p className="guide-live-label">A chooser may only point a sentence at a form item and say who said it. Fixed rules decide what counts, compute the gap and pick the wording. Only code marks an item filled in: a form value that passes the rule check, or a closed value the rule layer reads from your own words, which you confirm in the summary. Your text and form values are not stored.</p></details>
    </section> : null}
  </Disclosure>;
}
