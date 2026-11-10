import { lazy, Suspense, useCallback, useEffect, useMemo, useReducer, useRef, useState } from 'react';
import { ApiError, apiRequest, paypalIssueLines, retrySecondsLeft } from './api.js';
import ReferencePanel from './ReferencePanel.jsx';
import PolicyPanel from './PolicyPanel.jsx';
import { downloadPseudonymizedEvidence } from './pseudonymizedExport.js';
import { downloadInternalReviewZip, INTERNAL_REVIEW_ZIP_CONTENTS } from './reviewZip.js';
import { operatorLabel, operatorLabels, restoredReviewText, reviewSubmissionLabel, sandboxReadbackLabel } from './operatorLabels.js';
import { initialProductConfirmation, productConfirmationReducer } from './productConfirmation.js';
import { createPortal } from 'react-dom';
import { createSendConfirmTokens, MISSING_CONFIRM_NOTICE, readyWithoutToken } from './sendConfirm.js';
import { approveLockReason, draftLockReason, sellerEvidenceOnFile, SELLER_EVIDENCE_TEXT, sendLockReason } from './lockReasons.js';
import { hostedCopy } from './hostedCopy.js';
import { resumedNotice } from './resumeNotice.js';
import { SPONSOR_MAP, sponsorHref } from './sponsorMap.js';
import GuideLive, { useWaitClock, waitFailureMessage, WaitLine } from './GuideLive.jsx';
import CountryRules, { hasPostalBan } from './CountryRules.jsx';
import ProductReference from './ProductReference.jsx';
import { color as tokenColor } from './theme/tokens.js';
import { tabKeyDown } from './tabKeys.js';
import { displayDisputeId } from './disputeDisplay.js';

const AnalyticsDashboard = lazy(() => import('./AnalyticsDashboard.jsx'));
const GuideReplay = lazy(() => import('./GuideReplay.jsx'));
const RecordedSendReplay = lazy(() => import('./RecordedSendReplay.jsx'));
const VelocityChart = lazy(() => import('./charts/VelocityChart.jsx'));
const EvidenceBoard = lazy(() => import('./board/EvidenceBoard.jsx'));
// AG Grid and the time-evidence table load on demand (spec D13): the entry chunk carries no AG Grid code.
const AgGridReact = lazy(() => import('./grid/agGrid.jsx'));
const TimeEvidenceView = lazy(() => import('./TimeEvidenceView.jsx'));

// Plain Quartz params; grid/agGrid.jsx turns them into the theme when the grid loads.
// Colours come from the design tokens (review r1 P1.14), not a separate slate/teal set.
const gridTheme = ({
  backgroundColor: tokenColor.panel, foregroundColor: tokenColor.ink, borderColor: tokenColor.rule,
  headerBackgroundColor: tokenColor.recede, headerTextColor: tokenColor.muted, accentColor: tokenColor.accent,
  fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif', fontSize: 15,
  wrapperBorderRadius: 12, rowHoverColor: tokenColor.accentTint, cellHorizontalPadding: 18,
});

function Icon({ name, size = 18, ...props }) {
  const paths = {
    shield: <><path d="M12 3.25 4.75 6.25v5.5c0 4.85 3.1 7.95 7.25 9 4.15-1.05 7.25-4.15 7.25-9v-5.5L12 3.25Z" /><path d="m9 12.25 2.1 2.1 4.15-4.35" /></>,
    arrow: <><path d="M4.75 12h14.5" /><path d="m13.5 6.25 5.75 5.75-5.75 5.75" /></>,
    bolt: <path d="M13.25 3.25 5.5 13.5h5.75l-1 7.25 8.25-10.25h-5.75l.5-7.25Z" />,
    chart: <><path d="M4.25 4.75v14.5h15.5" /><path d="m7.5 15.25 3.5-4.25 3.25 2.5 4.5-6" /><circle cx="18.75" cy="7.5" r="1.25" /></>,
    check: <path d="m5.25 12.5 4.25 4.25 9.25-9.5" />,
    clock: <><circle cx="12" cy="12" r="8.5" /><path d="M12 7.5v4.75l3.25 2" /></>,
    layers: <><path d="m12 3.75 8.25 4.5-8.25 4.5-8.25-4.5L12 3.75Z" /><path d="m3.75 12.25 8.25 4.5 8.25-4.5" /><path d="m3.75 16.25 8.25 4.5 8.25-4.5" /></>,
    file: <><path d="M14.25 3.5H6.75a1.5 1.5 0 0 0-1.5 1.5v14a1.5 1.5 0 0 0 1.5 1.5h10.5a1.5 1.5 0 0 0 1.5-1.5V8L14.25 3.5Z" /><path d="M14 3.5v4.75h4.75M8.75 13h6.5M8.75 16.5h4.5" /></>,
    refresh: <><path d="M19.75 5.25v4.5h-4.5M4.25 18.75v-4.5h4.5" /><path d="M5.5 9.25a7.5 7.5 0 0 1 12.6-2.4l1.65 2.9M18.5 14.75a7.5 7.5 0 0 1-12.6 2.4l-1.65-2.9" /></>,
    link: <><path d="m9.75 14.25 4.5-4.5" /><path d="M8.5 16.25 7.25 17.5a3.75 3.75 0 0 1-5.3-5.3L5.2 8.95a3.75 3.75 0 0 1 5.3 0M15.5 7.75 16.75 6.5a3.75 3.75 0 0 1 5.3 5.3l-3.25 3.25a3.75 3.75 0 0 1-5.3 0" /></>,
    alert: <><path d="M10.7 4.2a1.5 1.5 0 0 1 2.6 0l7.45 13.3a1.5 1.5 0 0 1-1.3 2.25H4.55a1.5 1.5 0 0 1-1.3-2.25L10.7 4.2Z" /><path d="M12 9.25v4.25M12 16.75h.01" /></>,
    lock: <><rect x="5.25" y="10.25" width="13.5" height="10" rx="2" /><path d="M8.25 10.25V7a3.75 3.75 0 0 1 7.5 0v3.25M12 14v2.5" /></>,
    close: <path d="m6.5 6.5 11 11M17.5 6.5l-11 11" />,
    info: <><circle cx="12" cy="12" r="8.5" /><path d="M12 11v5.25M12 7.75h.01" /></>,
  };
  return <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" {...props}>{paths[name] || paths.shield}</svg>;
}

function Badge({ children, tone = 'muted', dot = false }) {
  return <span className={`badge badge-${tone}`}>{dot && <span className="status-dot" />}{children}</span>;
}

// One wording and one style for the stages where the seller decides (01 and 03).
function RoleBadge() {
  return <span className="badge badge-role" data-testid="role-badge"><Icon name="check" size={12} /> You review</span>;
}

// While its own action runs, a button stays focusable (aria-disabled, clicks ignored) so keyboard focus does not
// drop to the top of the page (review r1 P0.7); every other disabled state is a real `disabled`.
// `blocked` (attack r22): visibly disabled and aria-disabled, but it still takes the click, so the handler can point at
// the message that says why (a description over 200 characters was a dead click).
// `waiting` (attack r23): the same blocked state while a 429/503 Retry-After for this action runs.
function Button({ children, icon, tone = 'secondary', loading = false, blocked: blockedProp = false, waiting = false, className = '', disabled, onClick, ...props }) {
  const busyHold = Boolean(loading);
  const blocked = blockedProp || waiting;
  return <button className={`button button-${tone}${className ? ` ${className}` : ''}${blocked && !busyHold ? ' is-blocked' : ''}`} {...props} disabled={busyHold ? undefined : disabled}
    aria-disabled={busyHold || blocked || undefined} onClick={busyHold ? (event) => event.preventDefault() : onClick} aria-busy={loading}>{loading ? <span className="spinner" /> : icon && <Icon name={icon} size={16} />}{children}</button>;
}

// Top-bar Sandbox card (owner 2026-11-03): orange "Connect" face flips over to a green "connected" face with a
// breathing dot. Local runs only; the step 01 button does the same connect.
function TopbarSandbox({ connected, disabled, loading, onConnect }) {
  return <span className={`topbar-sandbox${connected ? ' is-connected' : ''}`} data-testid="topbar-sandbox" aria-live="polite">
    <Button className="topbar-sandbox-face topbar-sandbox-front" data-testid="topbar-sandbox-connect" tone="blue" disabled={disabled || connected} loading={loading} onClick={onConnect} aria-hidden={connected || undefined} tabIndex={connected ? -1 : undefined}>{!loading && <span className="topbar-sandbox-breath" />}<span className="topbar-sandbox-full">Connect US Sandbox</span><span className="topbar-sandbox-short">Sandbox</span></Button>
    <span className="topbar-sandbox-face topbar-sandbox-back" data-testid="topbar-sandbox-status" aria-hidden={connected ? undefined : true}><span className="topbar-sandbox-breath" /><span className="topbar-sandbox-full">Sandbox connected</span><span className="topbar-sandbox-short">Connected</span></span>
  </span>;
}

// "Start here" box: each button opens that situation's own live guide in its own step (hash #guide-<situation>).
const START_HERE = [['preflight', 'shield', 'Policy pre-check'], ['velocity', 'chart', 'Sales spike'], ['dispute', 'file', 'Dispute evidence']];
// Phone labels: one line each, never cut mid-word (owner 2026-11-03: wrapping looked broken).
const SHORT_LABEL = { 'Policy pre-check': 'Policy', 'Sales spike': 'Sales', 'Dispute evidence': 'Dispute' };
const Label = ({ text }) => <><span className="label-full">{text}</span><span className="label-short">{SHORT_LABEL[text] || text}</span></>;
const GUIDE_STAGE = { preflight: 'compliance', velocity: 'velocity', dispute: 'disputes' };

function StageAccordion({ id, number, title, subtitle, icon, status, actions, open, onOpen, children }) {
  const triggerId = `stage-trigger-${id}`;
  const contentId = `stage-content-${id}`;
  return <section id={id} className={`panel stage-accordion stage-${number} ${open ? 'is-open' : 'is-collapsed'}`}>
    {/* A plain heading: the step navigator above switches steps, so this header no longer pretends to collapse. */}
    <div className="stage-heading"><h2 id={triggerId} tabIndex={-1} data-testid={`stage-header-${id}`} className="stage-trigger stage-header"><span className="stage-trigger-label"><span className="stage-number">{number}</span><span><span className="stage-title"><Icon name={icon} size={19} />{title}</span><small>{subtitle}</small></span></span></h2><div className="stage-trigger-meta">{actions}{status}</div></div>
    <div id={contentId} className="stage-content" role="region" aria-labelledby={triggerId} hidden={!open}>{children}</div>
  </section>;
}

function OptionalDisclosure({ id, title, subtitle, icon, badge, open, onToggle, children, testId, level = 2 }) {
  const triggerId = `${id}-trigger`;
  const contentId = `${id}-content`;
  const Heading = level === 3 ? 'h3' : 'h2';
  return <section id={id} className={`optional-disclosure ${level === 3 ? 'step-section' : ''} ${open ? 'is-open' : ''}`}>
    <Heading className="optional-heading"><button id={triggerId} data-testid={testId} className="optional-trigger" type="button" aria-expanded={open} aria-controls={contentId} onClick={() => onToggle(!open)}><span><Icon name={icon} size={18} /><span><strong>{title}</strong><small>{subtitle}</small></span></span><span className="optional-trigger-meta">{badge}<span className="stage-chevron" aria-hidden="true" /></span></button></Heading>
    <div id={contentId} className="optional-content" role="region" aria-labelledby={triggerId} hidden={!open}>{children}</div>
  </section>;
}

// A collapsible section inside a step (level 2 of the console): an h3 under the step's h2.
const StepSection = (props) => <OptionalDisclosure {...props} level={3} />;

// One "More" disclosure per step (review r1 P1.10): sources, limits, examples and technical details sit here,
// closed by default, so the step itself shows only what a seller acts on.
function StepMore({ id, children }) {
  return <details className="step-more" data-testid={`step-more-${id}`}><summary><span>More: sources, limits, examples</span></summary><div className="step-more-body">{children}</div></details>;
}

function LimitsDrawer({ id, children }) {
  return <details className="limits-drawer" data-testid={`limits-drawer-${id}`}><summary className="limits-trigger"><span className="badge badge-muted"><Icon name="shield" size={14} /> Limits and safety</span><span className="stage-chevron" aria-hidden="true" /></summary><div className="limits-drawer-body">{children}</div></details>;
}

const SECONDARY_TABS = [['reference', 'Official sources'], ['policy', 'Policy check'], ['ai', 'AI brief'], ['tech', 'Technical details']];
function SecondaryStageTabs({ stage, activeTab, onSelectTab, referenceProps, aiAvailable, brief, notice, aiLoading, onGenerateAi, techContent, hosted = false }) {
  const tab = activeTab || 'reference';
  return <div className="secondary-area" data-testid={`secondary-area-${stage}`}>
    <div className="secondary-tabs" role="tablist" aria-label="Secondary tools" onKeyDown={(event) => tabKeyDown(event, SECONDARY_TABS.map(([key]) => key), tab, (key) => onSelectTab(stage, key, true), (key) => `secondary-tab-${stage}-${key}`)}>
      {SECONDARY_TABS.map(([key, label]) => <button key={key} id={`secondary-tab-${stage}-${key}`} type="button" role="tab" aria-selected={tab === key} tabIndex={tab === key ? 0 : -1} className={`secondary-tab ${tab === key ? 'is-active' : ''}`} onClick={() => onSelectTab(stage, key, true)}>{label}</button>)}
    </div>
    <div className="secondary-tab-pane" role="tabpanel" hidden={tab !== 'reference'}>
      <ReferencePanel theme={stage} {...referenceProps} open={true} onToggle={(nextOpen) => onSelectTab(stage, 'reference', nextOpen)} />
    </div>
    <div className="secondary-tab-pane" role="tabpanel" hidden={tab !== 'policy'}>
      <PolicyPanel theme={stage} {...referenceProps} open={true} onToggle={(nextOpen) => onSelectTab(stage, 'policy', nextOpen)} />
    </div>
    <div className="secondary-tab-pane" role="tabpanel" hidden={tab !== 'ai'}>
      <AiBriefPanel stage={stage} available={aiAvailable} brief={brief} notice={notice} loading={aiLoading} onGenerate={onGenerateAi} hosted={hosted} />
    </div>
    <div className="secondary-tab-pane secondary-tech-pane" role="tabpanel" hidden={tab !== 'tech'}>
      {techContent}
    </div>
  </div>;
}

// (r34 #15) Visible times use the viewer's own clock, like the "Stopped at 22:07" and countdown lines beside them;
// the fixed UTC form (utcLabel) stays in Technical details only.
function dateLabel(value) {
  if (!value) return '—';
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? '—' : date.toLocaleString('en-US', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hourCycle: 'h23', timeZoneName: 'short' });
}
function utcLabel(value) {
  if (!value) return '—';
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? '—' : `${date.toLocaleString('en-US', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false, timeZone: 'UTC' })} UTC`;
}
// (r34 #15) "valid for 1:12" (relative, ticking once a second) instead of a UTC end time; "expired" once it passed.
function ValidFor({ expiresAt, testId }) {
  const end = Date.parse(expiresAt || '');
  const [now, setNow] = useState(() => Date.now());
  useEffect(() => {
    if (!Number.isFinite(end)) return undefined;
    const interval = window.setInterval(() => { const at = Date.now(); setNow(at); if (at >= end) window.clearInterval(interval); }, 1000);
    return () => window.clearInterval(interval);
  }, [end]);
  if (!Number.isFinite(end)) return null;
  const left = Math.ceil((end - now) / 1000);
  return <span data-testid={testId}>{left > 0 ? `valid for ${Math.floor(left / 60)}:${String(left % 60).padStart(2, '0')}` : 'expired'}</span>;
}

// "Respond in 2 days" on each case card (UI/UX r16 P1: the three sample cases looked identical and the deadline only
// showed after a draft existed). Whole days left, rounded up; past due says so.
function dueLabel(value) {
  const due = Date.parse(value || '');
  if (!Number.isFinite(due)) return '';
  const days = Math.ceil((due - Date.now()) / 86400000);
  return days < 0 ? 'Response overdue' : days === 0 ? 'Respond today' : `Respond in ${days} day${days === 1 ? '' : 's'}`;
}

function sandboxEvidenceLabel(receipt) {
  return operatorLabel(receipt?.evidence_class, 'Connection not verified');
}

// PayPal's own seller_protection_eligible flag, shown only for Sandbox readbacks; the sample cases carry invented
// values, so they show no flag (PayPal-side review 2026-11-03 F3). Evidence never decides eligibility.
function sellerProtectionLabel(detail) {
  if (detail?.source !== 'paypal_sandbox') return 'PayPal decides if it applies';
  const flags = (detail.disputed_transactions || []).map((row) => row.seller_protection_eligible);
  const flag = flags.includes(true) ? 'eligible' : flags.includes(false) ? 'not eligible' : 'not stated';
  return `PayPal flag: ${flag} (PayPal decides)`;
}

function velocityStageStatusLabel(velocity) {
  if (velocity?.status === 'review_velocity') return 'Needs fulfillment review';
  if (velocity?.status === 'normal') return 'No review signal';
  return 'Baseline unavailable';
}

function AiBriefPanel({ stage, available, brief, loading, onGenerate, notice, hosted = false }) {
  const [open, setOpen] = useState(false);
  useEffect(() => { if (brief) setOpen(true); }, [brief]);
  return <section className="ai-brief-panel" data-testid={`ai-brief-${stage}`}>
    <div className="ai-brief-heading"><div><span className="meta-label">AI EVIDENCE BRIEF</span><h3>{brief ? 'Generated evidence brief' : 'Evidence summary (sample)'}</h3></div>{hosted ? null : <Button data-testid={`ai-generate-${stage}`} icon="layers" tone="secondary" loading={loading} disabled={!available || loading || Boolean(brief)} onClick={() => onGenerate(stage)}>{brief ? 'AI brief generated' : 'Generate AI brief'}</Button>}</div>{hosted && <p className="hosted-note" data-testid={`hosted-note-ai-${stage}`}>{HOSTED_NOTES.ai}</p>}{notice && <p className="ai-boundary" data-testid={`ai-notice-${stage}`} role="status">{notice}</p>}
    <details className="ai-brief-details" open={open} onToggle={(event) => setOpen(event.currentTarget.open)}><summary>{brief ? 'View evidence, citations, and limitations' : 'What the AI can and can\'t do'}</summary><div className="ai-brief-detail-body"><p className="ai-boundary">Uses fixed synthetic facts, pinned citation IDs and closed values the backend computes from this demo session (review categories, capture count and ratio, the selected case's evidence status). No description text, order, amount or identifier is sent. On the hosted demo the brief never calls the model. The backend permits at most three model attempts per process and one attempt per stage; failed attempts count and no automatic retry occurs. AI makes no compliance or dispute decision and authorizes no PayPal action.</p>{!available && !hosted && <p className="text-dim">Run the rule check first; then you decide whether to ask the AI.</p>}{brief && <div className="ai-brief-result" aria-live="polite"><div className="ai-brief-badges"><Badge tone="blue">AI GENERATED</Badge><Badge tone="blue">{brief.model}</Badge><Badge tone="muted">{operatorLabel(brief.prompt_contract_id)}</Badge><Badge tone="muted">{operatorLabel(brief.execution_evidence)}</Badge><Badge tone="amber">HUMAN REVIEW REQUIRED</Badge></div><p className="ai-summary">{brief.brief.summary}</p><div className="ai-brief-columns"><div><strong>Evidence points</strong><ul>{brief.brief.evidence_points.map((item) => <li key={item}>{item}</li>)}</ul></div><div><strong>Missing evidence</strong><ul>{brief.brief.missing_evidence.map((item) => <li key={item}>{item}</li>)}</ul></div></div><p className="ai-citations">Source references: {brief.brief.citation_ids.join(' · ')}</p><ul className="ai-limitations">{brief.limitations.map((item) => <li key={item}>{item}</li>)}</ul><p className="ai-authority">{operatorLabel(brief.compliance_decision)} · {operatorLabel(brief.current_policy_applicability)} · {operatorLabel(brief.semantic_entailment)} · {operatorLabel(brief.external_action_authorized === false ? 'EXTERNAL_ACTION_FALSE' : '')}</p></div>}</div></details>
  </section>;
}

// Hidden when the category check is switched off (the hosted demo forces it off), so the page does not show a
// "not available" line for a feature that is deliberately absent (Q30).
const categorySignalLabel = (result) => {
  if (result?.status === 'LOADING') return 'Category check: checking';
  if (!result || result.status !== 'SIGNAL') return 'Category check: not available';
  if (result.signal.category === null) return 'Category check: no matching category';
  return `Category check: ${result.signal.category} · ${result.signal.confidence === 'HIGH' ? 'high' : 'low'} confidence · advisory only, the rule result is unchanged`;
};
const AUP_POLICY_URL = 'https://www.paypal.com/us/legalhub/paypal/acceptableuse-full';
const NOTICE_DISMISS_MS = 4000;
const AI_NOT_CONFIGURED_NOTICE = 'Gemini profile not configured; see README "Turning on Gemini". The console works without it.';

const COUNTRY_ERROR_CODES = ['country_rules_blocked', 'country_check_changed', 'country_amount_changed'];

// Client-side checks before a request (attack r21 desktop #7/#14, phone #4/#5): a plain field message instead of
// the server's generic 422 text. The invoice draft takes 200 description characters and an amount above 0 with at
// most two decimals (the backend pattern is 1-7 digits and exactly two decimals; "10" is sent as "10.00").
const DESCRIPTION_LIMIT = 200;
const INVOICE_AMOUNT = /^[0-9]{1,7}(\.[0-9]{1,2})?$/;
const invoiceAmountProblem = (value) => {
  const text = String(value || '').trim();
  if (!INVOICE_AMOUNT.test(text) || !(Number(text) > 0)) return 'Enter an amount above 0 like 10.00: digits only, at most two decimals.';
  return '';
};
const invoiceAmountValue = (value) => Number(String(value).trim()).toFixed(2);
const descriptionProblem = (value) => (value.length > DESCRIPTION_LIMIT
  ? `Shorten the description to ${DESCRIPTION_LIMIT} characters or fewer (now ${value.length}). Invoice drafts take ${DESCRIPTION_LIMIT}.` : '');
// Repeat clicks on a download within this window are ignored (attack r21 desktop #12: three clicks gave six files).
const DOWNLOAD_REPEAT_MS = 1000;
// The phone bar ignores a tap this soon after its action changed (attack r21 phone #3: a double tap on Check country
// rules became Continue to draft).
const PHONE_ACTION_SETTLE_MS = 600;
// (round2 X, C #4) The phone bar's send actions wait this long after they appear (see phoneSendHeld).
const PHONE_SEND_HOLD_MS = 1200;
const PHONE_SEND_KEYS = ['evidence-submit', 'tracking-submit'];
const PHONE_SEND_HOLD_TEXT = 'Ready in a moment: check the preview above first.';
// How long the in-page action stays shown after a text field loses focus, so the tap that blurred it still lands
// (attack r21 phone #1).
const TYPING_RELEASE_MS = 700;
// Focus moves (attack r22 desktop P1): one requestAnimationFrame was not enough; in headless Chrome the frame never
// came, so focus stayed on BODY after Reset demo from 02/03 and after Confirm local draft review. The move is tried
// at once, then again on the next frame or after FOCUS_RETRY_MS (whichever comes first), up to FOCUS_RETRIES times.
const FOCUS_RETRY_MS = 50;
const FOCUS_RETRIES = 40;
// Touch screens: focusing a field opens the keyboard, which covered half of the field message (attack r22 phone #6).
const coarsePointer = () => window.matchMedia('(pointer: coarse)').matches;
// After the next render: the next frame or FOCUS_RETRY_MS, whichever comes first (a frame alone may never come).
const afterRender = (run) => { let done = false; const once = () => { if (!done) { done = true; run(); } }; window.requestAnimationFrame(once); window.setTimeout(once, FOCUS_RETRY_MS); };
const isTextEntry = (element) => element instanceof HTMLTextAreaElement
  || (element instanceof HTMLInputElement && !['checkbox', 'radio', 'button', 'submit', 'reset', 'range', 'color', 'file', 'hidden'].includes(element.type));

// Hosted demo (GET /connections answers mode "hosted_demo"): the controls that would reach PayPal or Gemini are not
// rendered; each is replaced by one line. The backend still answers 503 hosted_demo_disabled as a second guard.
const HOSTED_README_URL = 'https://github.com/jiarong0423/payguard-ai#run-locally';
const HOSTED_VIDEO_URL = 'https://youtu.be/upx5eZYOmC0';
const HOSTED_NOTES = {
  sandbox: 'Sandbox connect is off in the hosted demo. Run locally to connect your own Sandbox app.',
  invoice: 'Sandbox drafts are created only in a local run.',
  ai: 'AI brief is off in the hosted demo (no model calls). The sample summary below shows the format.',
  disputes: 'Sample cases (not real). The hosted demo does not read a Sandbox account.',
  paused: 'Refresh paused. Reload to resume.',
  evidence: 'Evidence requests are built and sent only in a local run.',
  // (2026-11-10) Hosted evidence send: nothing left to send, or the shared cap is used up.
  noneLeft: 'No Sandbox test dispute is waiting for a seller response right now, so there is nothing left to send here. The recorded replay below shows the same send.',
  capped: 'The shared limit for hosted evidence sends is used up for now. The recorded replay below shows the same send.',
};
// The product text that fits the country example (United States to Singapore, e-cigarettes); synthetic.
const EXAMPLE_DESCRIPTION = 'Rechargeable e-cigarette starter kit (synthetic example)';
const HOSTED_DISABLED_NOTICE = 'This needs a local run: on the hosted demo, invoice drafts, tracking and the AI brief are off.';

// (attack r23) The demo session survives the top-bar Dashboard link, a reload and Back: its id and CSRF token are kept
// in sessionStorage and resumed with GET /demo/state; a 401 (expired or evicted) starts a new session as before.
// sessionStorage is per tab: a new tab starts empty and creates its own session, so tabs stay isolated (only the
// browser's "Duplicate tab" copies it, and the copy then shares the tab's session). The values go nowhere except the
// headers the console already sends. Every access is wrapped in try/catch (private mode, blocked site data); without
// storage the console works as before, only without resume.
const SESSION_STORE_KEY = 'payguard.console.session.v1';
// The seller's own inputs (description text, selected case), never a check result.
const INPUT_STORE_KEY = 'payguard.console.inputs.v1';
const RAN_STORE_KEY = 'payguard.console.step1ran.v1';
// (fix r1 F1) The receipt of a send made in this tab's session, per dispute: the send response the page already showed
// (masked ids, PayPal-Debug-Id, file names and fingerprints) and the read-back status. Kept so the SUBMITTED card
// comes back after another dispute is opened or the page reloads; tied to the session id and never sent anywhere.
const SENT_STORE_KEY = 'payguard.console.sent.v1';
const tabStorage = () => { try { return window.sessionStorage; } catch { return null; } };
const readStored = (key) => {
  try { const raw = tabStorage()?.getItem(key); const value = raw ? JSON.parse(raw) : null; return value && typeof value === 'object' && !Array.isArray(value) ? value : null; }
  catch { return null; }
};
const writeStored = (key, value) => {
  try { if (value === null) tabStorage()?.removeItem(key); else tabStorage()?.setItem(key, JSON.stringify(value)); }
  catch { /* storage unavailable: no resume */ }
};
// (round2 X, B 2c) Keyed by the full dispute id the API returned (hosted code or raw local id). An older entry kept under
// a short form ("PP-R-…01", which two disputes can share) is dropped, never applied to a look-alike.
const storedReceipt = (id, row) => Boolean(typeof id === 'string' && !id.includes('…') && row && typeof row === 'object' && row.result && row.result.external_send === 'SUBMITTED'
  && row.result.dispute_id === id && typeof row.result.case_ref === 'string' && Array.isArray(row.result.files)
  && Array.isArray(row.result.input?.evidences) && row.result.input.evidences.every((part) => Array.isArray(part?.evidence_info?.tracking_info))
  && (row.result.sent_files == null || Array.isArray(row.result.sent_files)));
const readStoredReceipts = (sessionId) => {
  const value = readStored(SENT_STORE_KEY);
  if (!value || value.session_id !== sessionId || !value.items || typeof value.items !== 'object') return {};
  return Object.fromEntries(Object.entries(value.items).filter(([id, row]) => storedReceipt(id, row)));
};
// (round2 X, B 6a/6d) A receipt read back from this tab's storage is only a note: anyone with the tab can edit it. It is
// shown as SUBMITTED only when the fresh GET of the dispute (made when it is opened) reports it under review; otherwise
// its note is shown without the stamp and it locks nothing. The server keeps its own locks either way.
const RESTORED_SEND_STATUS = 'UNDER_REVIEW';
const restoredSendState = (stored, detail) => {
  if (!stored?.result || !detail || typeof detail.dispute_id !== 'string' || stored.result.dispute_id !== detail.dispute_id) return null;
  const sentAt = typeof stored.sent_at === 'string' && Number.isFinite(Date.parse(stored.sent_at)) ? stored.sent_at : null;
  return { dispute_id: detail.dispute_id, sent_at: sentAt, status: typeof detail.status === 'string' ? detail.status : null, confirmed: detail.status === RESTORED_SEND_STATUS };
};
const keptSendText = (restored) => `Kept in this tab from your send ${restored?.sent_at ? `at ${new Date(restored.sent_at).toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' })}` : 'earlier in this visit'}; PayPal read-back: ${operatorLabel(restored?.status, 'unavailable')}`;
const storedToken = (value) => typeof value === 'string' && /^[A-Za-z0-9_-]{16,128}$/.test(value);
const readStoredSession = () => {
  const value = readStored(SESSION_STORE_KEY);
  if (!value || !storedToken(value.session_id) || !storedToken(value.csrf_token) || !(Date.parse(value.expires_at) > Date.now())) return null;
  return { session_id: value.session_id, csrf_token: value.csrf_token, expires_at: value.expires_at, source: 'synthetic' };
};
const storeSession = (session) => writeStored(SESSION_STORE_KEY, session ? { session_id: session.session_id, csrf_token: session.csrf_token, expires_at: session.expires_at } : null);
const readStoredInputs = () => {
  const value = readStored(INPUT_STORE_KEY) || {};
  return { description: typeof value.description === 'string' && value.description.length <= 4000 ? value.description : null,
    case: typeof value.case === 'string' && /^case-ref-[0-9]{3}$/.test(value.case) ? value.case : '' };
};
// (attack r23) Shown as soon as the session's expires_at passes, not at the next click.
const SESSION_EXPIRED_TEXT = 'Session expired. Select Reconnect to start again; old results are cleared.';
// (owner 2026-11-10) After an expiry the console starts a new session by itself (expireSession), then says so.
const SESSION_RENEWED_TEXT = 'The demo session ended after 15 minutes without activity, so a new one started. Earlier results were cleared; run the step again.';
const AUTO_RENEW_LIMIT = 3;
const AUTO_RENEW_DELAY_MS = 1500;
// (owner 2026-11-10) The 2-minute policy check runs again by itself this long before it ends, up to 5 times in a row
// (one check per 2-minute window, inside the server's 5 open checks per 2 minutes).
const AUP_AUTO_RENEW_LEAD_MS = 3000;
const AUP_AUTO_RENEW_LIMIT = 5;
const AUP_RENEWED_TEXT = 'The 2-minute policy check ran again by itself for the same description.';
// (owner 2026-11-10) An unreviewed dispute draft is prepared again by itself shortly before its 5 minutes end. A
// recorded review is never renewed: it lapses with its draft and needs the seller again.
// The server returns an unexpired draft unchanged, so the renewal runs just after the window (store.py: 300 s).
const DRAFT_WINDOW_MS = 300000;
const DRAFT_AUTO_RENEW_AFTER_MS = DRAFT_WINDOW_MS + 1000;
const DRAFT_AUTO_RENEW_LIMIT = 5;
const DRAFT_RENEWED_TEXT = 'The evidence draft was prepared again by itself, so its 5-minute window started over. Nothing was sent.';
// (r31 J4 P1-1) The text comes from resumedNotice() (resumeNotice.js): only what the server still holds, and none
// at all for an empty session. It can be dismissed, so on a phone it never has to sit over the form for 10 s.
const RESUMED_INFO_MS = 10000;
// (r31 J4 P1-2 A3a) Shown inside the open draft dialog when the 120 s policy result behind it runs out.
const DRAFT_EXPIRED_TEXT = 'The check expired after 2 minutes. Run Policy Check again, then create the draft.';
// After Confirm Draft Context the button turns disabled; focus goes to the next step instead of the page (attack r23).
const AFTER_DRAFT_CONTEXT = ['[data-testid="invoice-create"]', '[data-testid="sandbox-connect"]', '[data-testid="phone-action-connect"]', '#compliance .stage-next .button'];

// The only hosted-demo control in the top bar: a pill that opens a fixed explanation. It calls no API.
// (r34 #1) Its Gemini wording comes from `guideChooser`, the chooser status the guide API returned (hostedCopy.js).
function HostedBadge({ guideChooser = null, sandboxReads = false, sandboxSend = false }) {
  const copy = hostedCopy(guideChooser, sandboxReads, sandboxSend);
  const [open, setOpen] = useState(false);
  const buttonRef = useRef(null);
  const popoverRef = useRef(null);
  useEffect(() => {
    if (!open) return undefined;
    const onKey = (event) => { if (event.key === 'Escape') { setOpen(false); buttonRef.current?.focus(); } };
    const onPointer = (event) => { if (!popoverRef.current?.contains(event.target) && !buttonRef.current?.contains(event.target)) setOpen(false); };
    const onScroll = () => setOpen(false);
    document.addEventListener('keydown', onKey);
    document.addEventListener('pointerdown', onPointer);
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => { document.removeEventListener('keydown', onKey); document.removeEventListener('pointerdown', onPointer); window.removeEventListener('scroll', onScroll); };
  }, [open]);
  return <>
    <button ref={buttonRef} type="button" className="badge badge-muted hosted-badge" data-testid="connections-hosted" aria-expanded={open} aria-controls="connections-why" onClick={() => setOpen((current) => !current)}><Icon name="info" size={14} /><span className="hosted-label-full">{copy.pill}</span><span className="hosted-label-short">Hosted demo</span><span className="hosted-why-cue">Why?</span></button>
    {open && <div ref={popoverRef} id="connections-why" className="hosted-why" data-testid="connections-why" role="dialog" aria-labelledby="connections-why-title">
      <span className="meta-label">Why?</span>
      <h2 id="connections-why-title">Why is this a hosted demo?</h2>
      <p data-testid="connections-why-intro">{copy.intro}</p>
      <strong>Works here</strong>
      <ul className="hosted-why-list hosted-why-works">
        <li>Policy pre-check, sales spike and dispute evidence (rules + your review)</li>
        <li>Review file and review ZIP downloads</li>
        <li>{copy.guides}</li>
      </ul>
      <strong>Local only</strong>
      <ul className="hosted-why-list hosted-why-local">
        <li>{sandboxSend ? 'Sandbox invoice draft and tracking' : sandboxReads ? 'Sandbox draft, evidence, tracking' : 'PayPal Sandbox connect, invoice draft, evidence request'}</li>
        <li>{copy.local}</li>
      </ul>
      <dl className="hosted-why-status"><div><dt>PayPal Sandbox</dt><dd>{sandboxSend ? 'Reads + capped evidence send' : sandboxReads ? 'Read-only' : 'Local run only'}</dd></div><div><dt>Gemini</dt><dd data-testid="connections-why-gemini">{copy.gemini}</dd></div></dl>
      <p>Watch it in the <a href={HOSTED_VIDEO_URL} target="_blank" rel="noopener noreferrer">demo video</a>, or run it locally (<a href={HOSTED_README_URL} target="_blank" rel="noopener noreferrer">README › Run locally</a>).</p>
    </div>}
  </>;
}

const findingLabels = {
  unsupported_financial_promise: 'Unsupported return claim', weapons: 'Weapons-related goods',
  controlled_substances: 'Controlled substances', counterfeit_goods: 'Counterfeit goods', regulated_activity: 'Regulated activity',
};

export default function App() {
  const sessionRef = useRef(null);
  const mounted = useRef(true);
  // The warning dialog's history entry (attack r21 phone #2): open while it is up, ignore for the pop that removes it.
  const dialogPopRef = useRef({ open: false, ignore: false });
  const [state, setState] = useState(null);
  const [sandbox, setSandbox] = useState(null);
  // True only when the backend says this is the hosted demo; unknown or failed reads keep the local console.
  const [hosted, setHosted] = useState(false);
  // True only when /connections says the hosted demo may make read-only Sandbox calls (connect, list, detail).
  // null until GET /connections has answered: the top bar then makes no claim about PayPal calls either way.
  const [sandboxReads, setSandboxReads] = useState(null);
  // (2026-11-10) Hosted evidence send on (/connections sandbox_send), with the shared caps left (counts only).
  const [sandboxSend, setSandboxSend] = useState(false);
  const [sendState, setSendState] = useState(null);
  // Fresh GET of the dispute right after a send: { status, debug }.
  const [sendReadback, setSendReadback] = useState(null);
  // (round2 X, B 6a/6d) The open dispute's receipt came from this tab's storage: restoredSendState(...) or null.
  const [restoredSend, setRestoredSend] = useState(null);
  // Open by default so the AG Charts chart and the AG Grid table are on screen without an extra click.
  const [velocityFold, setVelocityFold] = useState(true);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState('');
  const [error, setError] = useState(null);
  const errorRef = useRef(null);
  errorRef.current = error;
  const [notice, setNotice] = useState('');
  // (attack r23) Neutral, lasting messages ("Already checked", "Session resumed"): { kind, text }, not the green toast.
  const [info, setInfo] = useState(null);
  // (attack r23) Retry-After per action: action key -> epoch ms until which that action's button is held.
  const [cooldown, setCooldown] = useState({});
  const cooldownRef = useRef(cooldown);
  cooldownRef.current = cooldown;
  const coolingNow = (key) => (cooldownRef.current[key] || 0) > Date.now();
  const holdAfter = (key, failure) => { if (retrySecondsLeft(failure)) setCooldown((current) => ({ ...current, [key]: failure.retryAt })); };
  // The boot path's one automatic retry after a 503 (epoch ms it runs at; 0 = none pending).
  const [bootRetryAt, setBootRetryAt] = useState(0);
  const bootRetryRef = useRef(0);
  const now = useWaitClock(Math.max(0, bootRetryAt, error?.retryAt || 0, ...Object.values(cooldown)));
  const waitLeft = (key) => Math.max(0, Math.ceil(((cooldown[key] || 0) - now) / 1000));
  // "Session resumed" is shown for RESUMED_INFO_MS; "Already checked" stays until the description changes.
  useEffect(() => {
    if (info?.kind !== 'resumed') return undefined;
    const timer = window.setTimeout(() => setInfo((current) => (current?.kind === 'resumed' ? null : current)), RESUMED_INFO_MS);
    return () => window.clearTimeout(timer);
  }, [info]);
  const inputsRef = useRef(null);
  if (inputsRef.current === null) inputsRef.current = readStoredInputs();
  const [aiBriefs, setAiBriefs] = useState({});
  const [aiBusyStage, setAiBusyStage] = useState('');
  const [analyticsOpen, setAnalyticsOpen] = useState(false);
  const [activeStage, setActiveStage] = useState('compliance');
  const nextStageFocusRef = useRef(null);
  const [analyticsExpanded, setAnalyticsExpanded] = useState(false);
  const [replayExpanded, setReplayExpanded] = useState(false);
  // (r33 M4) Open items in the Step 3 guide (0 when it has not started), shown as one line in the evidence draft.
  const [guideOpenItems, setGuideOpenItems] = useState(0);
  // (r34 #1) The guide API's chooser status (chooser_mode, model_requested), reported by any guide on the page.
  const [guideChooser, setGuideChooser] = useState(null);
  // (r34 #3) Masked dispute a case was really sent to (external_send SUBMITTED), apart from a preview-only pairing.
  const sentByCaseRef = useRef({});
  // (fix r1 F1) dispute id -> { result, readback } for sends made in this session (see SENT_STORE_KEY).
  const sentReceipts = useRef({});
  // (r34 #7) The server's reason for the last refused preview: { kind, dispute_id, case_ref, message }.
  const [previewRefusal, setPreviewRefusal] = useState(null);
  const [boardExpanded, setBoardExpanded] = useState(null);
  const [activityExpanded, setActivityExpanded] = useState(false);
  const [openSecondary, setOpenSecondary] = useState({ source_compliance: null, velocity_guard: null, dispute_mediation: null });
  const [aiNotices, setAiNotices] = useState({});
  const [providerDisputes, setProviderDisputes] = useState(null);
  const [providerDisputeDetail, setProviderDisputeDetail] = useState(null);
  const [evidencePreview, setEvidencePreview] = useState(null);
  const autoLoadedRef = useRef({ burst: false, dispute: false });
  // Bumped when the browser comes back online, so a failed automatic stage load runs again (attack r21).
  const [onlineCount, setOnlineCount] = useState(0);
  const bootstrapRef = useRef(null);
  const autoRenewCountRef = useRef(0);
  // (owner 2026-11-10) The policy check's automatic renewal: the latest scan and guard, and renewals in a row.
  const aupAutoRef = useRef(null);
  const aupAutoRenewsRef = useRef(0);
  // The same for the 5-minute dispute draft before its review is recorded.
  const draftAutoRef = useRef(null);
  const draftAutoRenewsRef = useRef(0);
  const aupQuietRef = useRef(false);
  const draftQuietRef = useRef(false);
  const bootingRef = useRef(false);
  const providerDisputesKeyRef = useRef('');
  const toggleSecondary = useCallback((theme, panel, nextOpen) => {
    setOpenSecondary((current) => {
      if (nextOpen) return current[theme] === panel ? current : { ...current, [theme]: panel };
      return current[theme] === panel ? { ...current, [theme]: null } : current;
    });
  }, []);
  const [guideRequest, setGuideRequest] = useState(null);
  // Per-country rules (PayPal plus government and postal) for the seller/buyer pair; a BLOCK keeps the invoice draft closed (pre-block).
  const [countryCheck, setCountryCheck] = useState(null);
  const countryBlocked = Boolean(countryCheck?.blocked);
  // A Stop whose result was cleared by an edit, with no new check yet: the server still holds the Stop, so the page
  // keeps showing it (red team 2026-11-03 P1-1: the draft block used to open and the step turned green).
  const [countryStale, setCountryStale] = useState(false);
  // (optimise r24) The last country check result with its time and session, for the "From step 01" block in step 03;
  // an edit clears countryCheck but not this.
  const [lastCountryCheck, setLastCountryCheck] = useState(null);
  // A check ran earlier in this tab; results are never kept, so after a reload the page says so instead of resetting silently.
  const [clearedOnReload, setClearedOnReload] = useState(() => Boolean(readStored(RAN_STORE_KEY)));
  // (r34 #21) A check from an earlier session (Reconnect after it expired) is gone with it: say so where it was.
  const countryLost = Boolean(state && lastCountryCheck && lastCountryCheck.session !== state.session_id && !countryCheck);
  // (optimise r24) Add-tracking preview for an item-not-received case (POST /paypal/disputes/add-tracking).
  const [trackingPreview, setTrackingPreview] = useState(null);
  // (r25 send guard) The open double-confirm dialog ('evidence' or 'tracking'), and the dispute each case was paired
  // with in this page (from the server's send_guard), so a different dispute is held before any request.
  const [sendConfirm, setSendConfirm] = useState(null);
  // (foolproofing 2026-11-04) A real Sandbox draft and a Reset demo each need a confirmation dialog first.
  const [draftConfirm, setDraftConfirm] = useState(false);
  const [resetConfirm, setResetConfirm] = useState(false);
  // (r31 J4 P1-2) True while the open draft dialog's policy result has expired: the dialog stays and says so.
  const [draftExpired, setDraftExpired] = useState(false);
  const draftConfirmRef = useRef(false);
  draftConfirmRef.current = draftConfirm;
  // (r31 A3c) The last policy result ran out (not just "never run"), so the locked draft buttons can say why.
  const [aupExpired, setAupExpired] = useState(false);
  const boundByCaseRef = useRef({});
  // (r30 J2 P2-1, r31 J5 A6) The server's single-use send confirmation from the dialog's last re-check, per kind
  // (sendConfirm.js).
  const sendConfirmTokens = useRef(null);
  if (sendConfirmTokens.current === null) sendConfirmTokens.current = createSendConfirmTokens();
  const countryHeld = countryBlocked || countryStale;
  // Bumped by Reset demo so the country form starts empty again (click-all 2026-11-03 #2).
  const [countryResetCount, setCountryResetCount] = useState(0);
  // The panel's own request state, so the phone bar's Check country rules shows loading and aria-busy (attack r22 phone #5).
  const [countryBusy, setCountryBusy] = useState(false);
  // Step 01 Sandbox draft block: closed until a check result exists and no country rule stops the sale (plan r2 A2).
  const [sandboxOpen, setSandboxOpen] = useState(false);
  // Step 02 shows the chart or the order table, one at a time (plan r2 B8).
  const [velocityView, setVelocityView] = useState('chart');
  // (optimise r24) Phones see the last hours before the spike, so the spike bar is not a hairline.
  const narrowScreen = useNarrowScreen();
  // Phones: the section in view picks the action bar's button (plan r2 A4).
  const [phoneSection, setPhoneSection] = useState('');
  const askGuide = useCallback((scenario) => setGuideRequest((current) => ({ scenario, n: (current?.n || 0) + 1 })), []);
  const openStage = useCallback((stage, { updateHash = false, scroll = false, focus = false } = {}) => {
    if (!['compliance', 'velocity', 'disputes'].includes(stage)) return;
    if (focus) nextStageFocusRef.current = stage;
    setActiveStage(stage);
    if (updateHash && window.location.hash !== `#${stage}`) window.history.pushState(null, '', `#${stage}`);
    if (scroll) window.requestAnimationFrame(() => {
      const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      document.getElementById(stage)?.scrollIntoView({ behavior: reducedMotion ? 'auto' : 'smooth', block: 'start' });
      // The stage is still opening when the first scroll starts, so the page can land too low; once it has settled,
      // bring the stage heading back to the top if it is not there.
      window.setTimeout(() => {
        const el = document.getElementById(stage);
        if (el && Math.abs(el.getBoundingClientRect().top) > 24) el.scrollIntoView({ behavior: 'auto', block: 'start' });
      }, 450);
    });
  }, []);
  useEffect(() => {
    const syncFromHash = () => {
      const target = window.location.hash.slice(1);
      if (['compliance', 'velocity', 'disputes'].includes(target)) setActiveStage(target);
      const guideTarget = START_HERE.find(([scenario]) => target === `guide-${scenario}`);
      if (guideTarget) { setActiveStage(GUIDE_STAGE[guideTarget[0]]); askGuide(guideTarget[0]); }
      setAnalyticsExpanded(target === 'analytics');
      // (fix r1 F7) The Sponsor map's Bryntum link: step 03 with the deadline board tab open.
      if (target === 'evidence-board') { setActiveStage('disputes'); setBoardExpanded(true); }
    };
    // The warning dialog's own history entry (attack r21) is not a navigation: popping it must not re-run a guide jump.
    const onPop = () => {
      if (dialogPopRef.current.open || dialogPopRef.current.ignore) { dialogPopRef.current.ignore = false; return; }
      syncFromHash();
    };
    syncFromHash();
    window.addEventListener('hashchange', syncFromHash);
    window.addEventListener('popstate', onPop);
    return () => {
      window.removeEventListener('hashchange', syncFromHash);
      window.removeEventListener('popstate', onPop);
    };
  }, []);
  useEffect(() => {
    if (nextStageFocusRef.current === activeStage) {
      nextStageFocusRef.current = null;
      document.getElementById(`stage-trigger-${activeStage}`)?.focus({ preventScroll: true });
      return;
    }
    const focused = document.activeElement;
    if (focused instanceof Element && focused.closest('.stage-content[hidden]')) {
      document.getElementById(`stage-trigger-${activeStage}`)?.focus();
    }
  }, [activeStage]);
  useEffect(() => {
    if (!notice) return undefined;
    const timer = window.setTimeout(() => setNotice(''), NOTICE_DISMISS_MS);
    return () => window.clearTimeout(timer);
  }, [notice]);
  useEffect(() => { if (!busy) flushFocus(); }, [busy]); // eslint-disable-line react-hooks/exhaustive-deps
  // Phones: "typing" replaces the CSS :focus switch that hid the action bar (attack r21 phone #1/#10). Leaving a text
  // field keeps it for TYPING_RELEASE_MS, so the in-page Run Policy Check or Check country rules stays visible and
  // tappable while the tap that blurred the field lands. When the keyboard closes with Back (the field keeps focus),
  // the field is blurred so the bar comes back.
  const [typing, setTyping] = useState(false);
  useEffect(() => {
    let timer = 0;
    let keyboardSeen = false;
    const onFocusIn = (event) => { if (isTextEntry(event.target)) { window.clearTimeout(timer); setTyping(true); } };
    const onFocusOut = (event) => {
      if (!isTextEntry(event.target)) return;
      window.clearTimeout(timer);
      timer = window.setTimeout(() => { if (!isTextEntry(document.activeElement)) { keyboardSeen = false; setTyping(false); } }, TYPING_RELEASE_MS);
    };
    const viewport = window.visualViewport;
    const coarse = window.matchMedia('(pointer: coarse)');
    const onViewport = () => {
      if (!viewport || !coarse.matches) return;
      const keyboardUp = window.innerHeight - viewport.height * viewport.scale > 120;
      if (keyboardUp) { keyboardSeen = true; return; }
      if (keyboardSeen && isTextEntry(document.activeElement)) { keyboardSeen = false; document.activeElement.blur(); }
    };
    document.addEventListener('focusin', onFocusIn);
    document.addEventListener('focusout', onFocusOut);
    viewport?.addEventListener('resize', onViewport);
    return () => {
      window.clearTimeout(timer);
      document.removeEventListener('focusin', onFocusIn);
      document.removeEventListener('focusout', onFocusOut);
      viewport?.removeEventListener('resize', onViewport);
    };
  }, []);
  const aiRevisionRef = useRef(0);
  const aiControllerRef = useRef(null);
  const invalidateAi = useCallback(() => {
    aiRevisionRef.current += 1;
    aiControllerRef.current?.abort();
    aiControllerRef.current = null;
    setAiBriefs({});
    setAiNotices({});
    setAiBusyStage('');
  }, []);
  const [description, setDescription] = useState(() => inputsRef.current.description ?? 'Handcrafted ceramic coffee cup — set of two');
  const [aup, setAup] = useState(null);
  const [aupPhase, setAupPhase] = useState('empty');
  const [aupConsumed, setAupConsumed] = useState(false);
  const [warningOpen, setWarningOpen] = useState(false);
  const aupRevisionRef = useRef(0);
  const aupControllerRef = useRef(null);
  const [categorySignal, setCategorySignal] = useState(null);
  const [sourcesOpen, setSourcesOpen] = useState({});
  const [productRef, setProductRef] = useState(null);
  // Kept apart from the AUP result: expiry of the check does not clear it (see productConfirmation.js).
  const [productConfirmation, dispatchProductConfirmation] = useReducer(productConfirmationReducer, initialProductConfirmation);
  const productConfirm = productConfirmation.record;
  const productConfirmationRef = useRef(productConfirmation);
  productConfirmationRef.current = productConfirmation;
  const categoryControllerRef = useRef(null);
  const busyRef = useRef('');
  const warningRef = useRef(null);
  // Focus that must wait until the running action ends (its button turns disabled at that point and would drop focus
  // to the page): approve -> receipt, Reset -> a visible control, dialog close -> Run Policy Check (attack r21
  // desktop #5/#6, phone #11). The first selector that is on screen and enabled wins.
  const focusAfterRef = useRef(null);
  // Bumped by every new focus request, so an older retry loop stops (attack r22).
  const focusTokenRef = useRef(0);
  const flushFocus = () => {
    const pending = focusAfterRef.current;
    if (!pending) return;
    focusAfterRef.current = null;
    const token = ++focusTokenRef.current;
    const usable = (element) => element && !element.disabled && element.getClientRects().length > 0 && window.getComputedStyle(element).visibility !== 'hidden';
    // Retries only while focus is lost (BODY, gone, or on a now-disabled control): a seller who moved on keeps focus.
    const lost = () => { const active = document.activeElement; return !active || active === document.body || !active.isConnected || active.disabled === true; };
    let tries = 0;
    const attempt = () => {
      if (token !== focusTokenRef.current || (tries > 0 && !lost())) return;
      const target = pending.selectors.map((selector) => document.querySelector(selector)).find(usable);
      if (target) {
        if (pending.scroll === true) target.scrollIntoView({ block: 'center', behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
        target.focus({ preventScroll: true });
        if (document.activeElement === target) {
          // One late check: a disabled button's blur or a re-render can still drop focus after this frame, and a
          // smooth scroll that never got its frames leaves the target off screen; then it jumps there ('instant', since
          // html has scroll-behavior: smooth).
          if (tries === 0) {
            tries = 1;
            window.setTimeout(() => {
              if (token !== focusTokenRef.current) return;
              if (lost()) { attempt(); return; }
              const box = target.getBoundingClientRect();
              if (pending.scroll && document.activeElement === target && (box.bottom <= 0 || box.top >= window.innerHeight)) target.scrollIntoView({ block: pending.scroll === true ? 'center' : 'nearest', behavior: 'instant' });
            }, pending.scroll === true ? FOCUS_RETRY_MS * 6 : FOCUS_RETRY_MS * 16);
          }
          return;
        }
      }
      tries += 1;
      if (tries > FOCUS_RETRIES) return;
      afterRender(attempt);
    };
    attempt();
  };
  // scroll: true scrolls the target to the middle; 'fallback' leaves the page's own scroll alone and only jumps when
  // the target is still off screen about 800 ms later (Reset demo: openStage already scrolls to step 01).
  const focusWhenIdle = (selectors, { scroll = false } = {}) => {
    focusTokenRef.current += 1;
    focusAfterRef.current = { selectors, scroll };
    if (!busyRef.current) flushFocus();
  };
  const invalidateAup = useCallback(() => {
    invalidateAi();
    aupRevisionRef.current += 1;
    aupControllerRef.current?.abort();
    aupControllerRef.current = null;
    categoryControllerRef.current?.abort();
    categoryControllerRef.current = null;
    setCategorySignal(null); setProductRef(null);
    setAup(null); setAupPhase('empty'); setAupConsumed(false); setWarningOpen(false);
    setInvoiceReview(null); setInvoice(null); setInvoiceChecked(false); setAupExpired(false);
    // "Already checked" belongs to the result it pointed at (attack r23).
    setInfo((current) => (current?.kind === 'already' ? null : current));
  }, [invalidateAi]);
  // Which action raised the current error banner, so an edit that fixes the cause can clear it (attack r21 phone #7).
  const errorSourceRef = useRef('');
  const editDescription = (value) => { invalidateAup(); dispatchProductConfirmation({ type: 'clear', reason: 'description_edited' }); setDescription(value); aupAutoRenewsRef.current = 0;
    // A policy-check error goes once the description is valid again (attack r21).
    if (errorSourceRef.current === 'aup' && value.trim() && value.length <= DESCRIPTION_LIMIT) { errorSourceRef.current = ''; setError((current) => (current && current.status !== 401 ? null : current)); }
  };
  useEffect(() => {
    if (!aup) return;
    // (r31 J1 J4 A3) A neutral "needs action" message (not the green success toast); the locked draft buttons say why,
    // and an open draft dialog stays with its own expiry line instead of closing on its own.
    const expire = () => {
      invalidateAup(); setAupExpired(true); if (draftConfirmRef.current) setDraftExpired(true);
      setNotice(''); setInfo({ kind: 'expired', text: 'The description check expired. Run it again before continuing.' });
    };
    // (owner 2026-11-10) Shortly before the 2-minute end the same check runs again by itself (same text, same rules),
    // so a seller reading the result does not have to press Run Policy Check. Not while a product confirmation, the
    // draft dialog or a confirmed draft context depends on this exact result, and at most AUP_AUTO_RENEW_LIMIT times in
    // a row without a press of the seller's own; otherwise it expires as before.
    let fallback = 0;
    const lead = Math.max(0, Date.parse(aup.expires_at) - Date.now() - AUP_AUTO_RENEW_LEAD_MS);
    const timer = setTimeout(() => {
      const auto = aupAutoRef.current;
      if (auto?.canRenew()) {
        aupAutoRenewsRef.current += 1;
        aupQuietRef.current = true;
        auto.scan().then((ok) => { aupQuietRef.current = false; if (ok) setInfo({ kind: 'resumed', text: AUP_RENEWED_TEXT }); });
        return;
      }
      fallback = setTimeout(expire, Math.max(0, Date.parse(aup.expires_at) - Date.now()));
    }, lead);
    return () => { clearTimeout(timer); clearTimeout(fallback); };
  }, [aup, invalidateAup]);
  // The draft block opens itself once a result makes it usable and closes again on a country Stop.
  const sandboxReady = Boolean(aup || countryCheck) && !countryHeld;
  useEffect(() => { setSandboxOpen(sandboxReady); }, [sandboxReady]);
  const continueToDraft = useCallback(() => {
    setSandboxOpen(true);
    window.requestAnimationFrame(() => {
      const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      document.getElementById('sandbox-draft')?.scrollIntoView({ behavior: reducedMotion ? 'auto' : 'smooth', block: 'start' });
      // Focus follows the scroll (red team 2026-11-03 P2-2), so the keyboard is not left on an off-screen button.
      document.querySelector('#sandbox-draft summary')?.focus({ preventScroll: true });
    });
  }, []);
  useEffect(() => {
    if (activeStage !== 'compliance') { setPhoneSection(''); return undefined; }
    const phone = window.matchMedia('(max-width: 640px)');
    // One rect read per scroll event; React skips the render when the section has not changed.
    // Enter at 60/30 % of the viewport, leave only past 70/20 %: without that gap the bar flipped between Run Policy
    // Check and Check country rules about 8 times a second at the boundary (phone click-all r2 P0).
    let current = '';
    const measure = () => {
      const rules = document.querySelector('[data-testid="country-rules"]')?.getBoundingClientRect();
      const height = window.innerHeight;
      const inside = Boolean(rules) && (current === 'country'
        ? rules.top < height * 0.7 && rules.bottom > height * 0.2
        : rules.top < height * 0.6 && rules.bottom > height * 0.3);
      current = phone.matches && inside ? 'country' : '';
      setPhoneSection(current);
    };
    const timer = window.setTimeout(measure, 0);
    window.addEventListener('scroll', measure, { passive: true });
    window.addEventListener('resize', measure);
    phone.addEventListener('change', measure);
    return () => {
      window.clearTimeout(timer);
      window.removeEventListener('scroll', measure);
      window.removeEventListener('resize', measure);
      phone.removeEventListener('change', measure);
    };
  }, [activeStage]);
  // How the warning dialog closed, so focus goes back to the right place (attack r21 phone #11).
  const warningCloseRef = useRef('');
  useEffect(() => {
    if (!warningOpen) return;
    const previous = document.activeElement;
    warningRef.current?.querySelector('button')?.focus();
    return () => {
      const how = warningCloseRef.current;
      warningCloseRef.current = '';
      // Acknowledge and continue: bindInvoice moves focus to the next step, or the failure path to Run Policy Check.
      if (how === 'ACKNOWLEDGE_AND_CONTINUE') return;
      if (how !== 'RETURN_TO_EDIT' && previous?.isConnected && !previous.disabled && !isTextEntry(previous)) { previous.focus(); return; }
      // Only "Return to edit" puts the caret in the description: Cancel flow or Back must not open the phone keyboard
      // (attack r21 phone #11); they land on the visible Run Policy Check button or the step heading instead.
      if (how === 'RETURN_TO_EDIT') { focusWhenIdle(['#description']); return; }
      focusWhenIdle(['[data-testid="aup-review"]', '[data-testid="phone-action-aup"]', '#stage-trigger-compliance']);
    };
  }, [warningOpen]);
  // Android Back with the dialog open closed the page and lost the session (attack r21 phone #2): the dialog owns one
  // history entry, Back pops it and only closes the dialog (the check result stays, nothing is acknowledged).
  useEffect(() => {
    if (!warningOpen) return undefined;
    let popped = false;
    dialogPopRef.current.open = true;
    window.history.pushState({ ...(window.history.state || {}), pgWarningDialog: true }, '');
    const onPop = () => {
      if (window.history.state?.pgWarningDialog) return;
      popped = true;
      warningCloseRef.current = 'BACK';
      setWarningOpen(false);
    };
    window.addEventListener('popstate', onPop);
    return () => {
      dialogPopRef.current.open = false;
      window.removeEventListener('popstate', onPop);
      if (!popped && window.history.state?.pgWarningDialog) { dialogPopRef.current.ignore = true; window.history.back(); }
    };
  }, [warningOpen]);
  const [selectedCase, setSelectedCase] = useState('');
  // The seller's inputs only (attack r23): the description and the selected case come back after a reload or Back.
  useEffect(() => { writeStored(INPUT_STORE_KEY, { description, case: selectedCase }); }, [description, selectedCase]);
  const [draft, setDraft] = useState(null);
  // Drafts fetched in this session, by case, so the deadline board keeps every prepared case on screen.
  const [boardDrafts, setBoardDrafts] = useState({ session: null, drafts: {} });
  useEffect(() => { const session = state?.session_id; if (draft?.case_ref && session) setBoardDrafts((current) => ({ session, drafts: { ...(current.session === session ? current.drafts : {}), [draft.case_ref]: draft } })); }, [draft, state?.session_id]);
  const [receipt, setReceipt] = useState(null);
  const [reviewChecked, setReviewChecked] = useState(false);
  const [invoiceAmount, setInvoiceAmount] = useState('10.00');
  const [invoiceReview, setInvoiceReview] = useState(null);
  const [invoice, setInvoice] = useState(null);
  const [invoiceChecked, setInvoiceChecked] = useState(false);
  const [velocityQuickFilter, setVelocityQuickFilter] = useState('');
  const [selectedVelocityTransaction, setSelectedVelocityTransaction] = useState(null);
  const editInvoiceAmount = (value) => {
    if (invoiceReview || invoice || aupConsumed) {
      invalidateAup();
      setNotice('Draft amount changed. Run Policy Check again before confirming the draft context.');
    } else {
      setInvoiceReview(null);
      setInvoice(null);
      setInvoiceChecked(false);
    }
    setInvoiceAmount(value);
    // The field message goes as soon as the amount is valid (attack r21); an amount error banner goes with it.
    if (!invoiceAmountProblem(value)) {
      setAmountNote('');
      if (errorSourceRef.current === 'invoice-review') { errorSourceRef.current = ''; setError((current) => (current && current.status !== 401 ? null : current)); }
    }
  };
  // A new country check after review changes the route the draft would carry, so the bound review is dropped
  // (red team 2026-11-03 F5); the server also answers 409 country_check_changed.
  // Editing a country field clears the result (onResult(null)); that also drops a bound review (GLM red team #8).
  // `stale` is set when an edit cleared a Stop result (the server still holds that Stop until a new check).
  const onCountryResult = (result, { stale = false } = {}) => {
    const hadCheck = Boolean(countryCheck);
    if (result) writeStored(RAN_STORE_KEY, { ran: true });
    setCountryCheck(result);
    setCountryStale(!result && stale);
    if (result) setLastCountryCheck({ session: sessionRef.current?.session_id || null, seller_country: result.seller_country, buyer_country: result.buyer_country,
      blocked: result.blocked, postal: hasPostalBan(result), at: Date.now() });
    // A new result replaces any earlier country error banner (red team 2026-11-03 P1-2: a 409 stayed after a pass).
    if (result) setError((current) => (COUNTRY_ERROR_CODES.includes(current?.code) ? null : current));
    if (invoiceReview && (result || hadCheck)) {
      invalidateAup();
      setNotice('Country details changed. Run Policy Check and confirm the draft context again.');
    }
  };
  const referenceRevisionRef = useRef(0);
  const [referenceRevision, setReferenceRevision] = useState(0);
  const invalidateReferences = useCallback(() => {
    referenceRevisionRef.current += 1;
    setReferenceRevision(referenceRevisionRef.current);
  }, []);
  const expireSession = useCallback((failure, identity, expectedRevision) => {
    if (sessionRef.current?.session_id !== identity || referenceRevisionRef.current !== expectedRevision) return;
    invalidateReferences();
    invalidateAup();
    sessionRef.current = null;
    storeSession(null);
    setInfo(null);
    dispatchProductConfirmation({ type: 'clear', reason: 'session_changed', session: null });
    setState(null); setDraft(null); setReceipt(null); setSelectedCase('');
    setReviewChecked(false); setAup(null); setInvoiceReview(null); setInvoice(null); setInvoiceChecked(false);
    setVelocityQuickFilter(''); setSelectedVelocityTransaction(null);
    sendConfirmTokens.current.clearAll();
    setError(failure);
    // (owner 2026-11-10) An expired session starts a new one by itself instead of waiting for Reconnect; the banner
    // shows for a moment, then a lasting notice says what was cleared. At most AUTO_RENEW_LIMIT times per page load.
    if (failure?.status === 401 && autoRenewCountRef.current < AUTO_RENEW_LIMIT) {
      autoRenewCountRef.current += 1;
      window.setTimeout(() => bootstrapRef.current?.({ renewed: true }), AUTO_RENEW_DELAY_MS);
    }
  }, [invalidateReferences, invalidateAup]);

  const bootstrap = useCallback(async (signal, { auto = false, renewed = false } = {}) => {
    bootingRef.current = true;
    window.clearTimeout(bootRetryRef.current); bootRetryRef.current = 0; setBootRetryAt(0);
    setInfo(null);
    invalidateReferences();
    invalidateAup();
    setLoading(true);
    setError(null);
    setState(null);
    sessionRef.current = null;
    dispatchProductConfirmation({ type: 'clear', reason: 'session_changed', session: null });
    setDraft(null);
    setReceipt(null);
    setAup(null);
    setSelectedCase('');
    setInvoiceReview(null);
    setInvoice(null);
    setInvoiceChecked(false);
    // A new session has no country check; an old Stop or pass must not carry over (red team r10 #3, r13 P2).
    setCountryCheck(null); setCountryStale(false);
    setVelocityQuickFilter('');
    setSelectedVelocityTransaction(null);
    autoLoadedRef.current = { burst: false, dispute: false };
    providerDisputesKeyRef.current = '';
    setProviderDisputes(null); setProviderDisputeDetail(null); setEvidencePreview(null);
    // (r31 J5) A new or resumed session starts with no send confirmation from an earlier one.
    sendConfirmTokens.current.clearAll();
    // (r34 #3) Pairings are per session on the server; a resumed one reports its own again at the next preview.
    sentReceipts.current = {}; boundByCaseRef.current = {}; sentByCaseRef.current = {}; setPreviewRefusal(null); setRestoredSend(null);
    try {
      // (attack r23) Resume this tab's session when the server still holds it; a 401 means it expired, so a new one
      // starts as before. Any other failure (busy, offline) keeps the stored id for the next try.
      const stored = readStoredSession();
      let session = null;
      let resumedState = null;
      if (stored) {
        try {
          resumedState = await apiRequest('/demo/state', { session: stored, signal });
          session = { ...stored, expires_at: resumedState.expires_at };
        } catch (failure) {
          if (failure.status !== 401) throw failure;
          storeSession(null);
        }
      }
      if (!session) session = await apiRequest('/demo/sessions', { method: 'POST', body: {}, signal });
      if (signal?.aborted || !mounted.current) return;
      sessionRef.current = session;
      storeSession(session);
      dispatchProductConfirmation({ type: 'clear', reason: 'session_changed', session: session.session_id });
      const [nextState, status, connections] = await Promise.all([
        resumedState || apiRequest('/demo/state', { session, signal }), apiRequest('/paypal/status', { session, signal }),
        apiRequest('/connections', { session, signal }).catch(() => null),
      ]);
      if (signal?.aborted || !mounted.current) return;
      // A failed /connections read is not proof of a local run (red team r13 P2): off this machine, treat it as hosted.
      setHosted(connections ? connections.mode === 'hosted_demo' : !['localhost', '127.0.0.1', '[::1]'].includes(window.location.hostname));
      setSandboxReads(connections?.mode === 'hosted_demo' && connections.sandbox_reads === true);
      setSandboxSend(connections?.mode === 'hosted_demo' && connections.sandbox_send === true);
      setSendState(connections?.send_state || null);
      if (resumedState) {
        // Only what the server holds comes back (attack r23): its drafts, read again with the same POST that returns an
        // existing draft unchanged, and a review the server records as done. Check results have no read, so they are
        // not rebuilt here.
        const prepared = nextState.disputes.filter((row) => ['draft_ready', 'local_draft_reviewed'].includes(row.status));
        const wanted = nextState.disputes.find((row) => row.case_ref === inputsRef.current.case) || prepared[0];
        const drafts = (await Promise.all(prepared.map((row) => apiRequest(`/disputes/${encodeURIComponent(row.case_ref)}/draft`,
          { method: 'POST', body: {}, session, signal }).catch(() => null)))).filter(Boolean);
        if (signal?.aborted || !mounted.current) return;
        if (drafts.length) setBoardDrafts({ session: session.session_id, drafts: Object.fromEntries(drafts.map((row) => [row.case_ref, row])) });
        if (wanted) setSelectedCase(wanted.case_ref);
        setDraft(drafts.find((row) => row.case_ref === wanted?.case_ref) || null);
        // (r31 J4 P1-1) Worded from what came back; an empty session (Reset demo, then reload) shows nothing.
        const resumed = resumedNotice(nextState, drafts);
        if (resumed) setInfo({ kind: 'resumed', text: resumed });
      }
      setState(nextState);
      setSandbox(status);
      if (renewed && !resumedState) setInfo({ kind: 'resumed', text: SESSION_RENEWED_TEXT });
    } catch (failure) {
      if (!signal?.aborted && mounted.current) {
        setError(failure);
        holdAfter('boot', failure);
        // (attack r23) A busy server (503 with Retry-After) gets one automatic retry once the wait is over.
        if (failure.status === 503 && retrySecondsLeft(failure) && !auto) {
          setBootRetryAt(failure.retryAt);
          bootRetryRef.current = window.setTimeout(() => { bootRetryRef.current = 0; setBootRetryAt(0); bootstrapRef.current?.({ auto: true }); }, failure.retryAt - Date.now());
        }
      }
    } finally {
      bootingRef.current = false;
      if (!signal?.aborted && mounted.current) setLoading(false);
    }
  }, [invalidateReferences, invalidateAup]);
  bootstrapRef.current = (options) => { if (!bootingRef.current && mounted.current) bootstrap(undefined, options); };
  // Reconnect: one request at a time, and none while a Retry-After runs (attack r23: three clicks sent three).
  const reconnect = () => { if (bootingRef.current || coolingNow('boot')) return; bootstrap(); };

  useEffect(() => {
    mounted.current = true;
    const controller = new AbortController();
    bootstrap(controller.signal);
    return () => { mounted.current = false; sessionRef.current = null; window.clearTimeout(bootRetryRef.current); aupControllerRef.current?.abort(); categoryControllerRef.current?.abort(); aiControllerRef.current?.abort(); controller.abort(); };
  }, [bootstrap]);

  // Resolves true only when the action finished without an error (the automatic stage loads retry otherwise; attack r21).
  const action = async (key, run) => {
    if (busyRef.current || !sessionRef.current || coolingNow(key)) return false;
    const identity = sessionRef.current.session_id;
    let revision = referenceRevisionRef.current;
    busyRef.current = key;
    setBusy(key);
    setError(null);
    errorSourceRef.current = '';
    setNotice('');
    setInfo((current) => (current?.kind === 'already' ? current : null));
    // Reset demo empties the session's evaluations on the server, so the confirmation's basis is gone too.
    if (key === 'reset') { invalidateReferences(); invalidateAup(); dispatchProductConfirmation({ type: 'clear', reason: 'session_changed', session: sessionRef.current?.session_id ?? null }); revision = referenceRevisionRef.current; }
    try { await run(sessionRef.current); return true; }
    catch (failure) {
      if (failure.code === 'request_cancelled' || sessionRef.current?.session_id !== identity) return;
      if (failure.code === 'hosted_demo_disabled') { setNotice(HOSTED_DISABLED_NOTICE); return; }
      holdAfter(key, failure);
      setError(failure);
      errorSourceRef.current = key;
      if (failure.status === 401) expireSession(failure, identity, revision);
      return false;
    }
    finally { busyRef.current = ''; if (mounted.current) setBusy(''); }
  };
  // The country panel and the guides report a 401 here, so they share the "Demo session expired + Reconnect" banner
  // with the rest of the console (attack r21 desktop #10).
  const panelSessionExpired = useCallback((failure, session) => {
    expireSession(failure, session?.session_id, referenceRevisionRef.current);
  }, [expireSession]);
  // (attack r23) The session has a fixed expires_at: once it passes, the page says so at once (it used to clear the
  // results silently and explain only at the next click). The server is asked first, so a clock that runs ahead does
  // not end a live session; offline or busy, it asks again shortly, and a minute past the time it ends anyway.
  useEffect(() => {
    const session = sessionRef.current;
    const expires = Date.parse(state?.expires_at || '');
    if (!state || !session || session.session_id !== state.session_id || !Number.isFinite(expires)) return undefined;
    let stopped = false;
    let timer = 0;
    let probing = false;
    const end = () => expireSession(new ApiError(SESSION_EXPIRED_TEXT, 401, 'session_expired'), session.session_id, referenceRevisionRef.current);
    const check = async () => {
      window.clearTimeout(timer);
      if (stopped || probing || sessionRef.current?.session_id !== session.session_id) return;
      const left = expires - Date.now();
      if (left > 0) { timer = window.setTimeout(check, Math.min(left + 250, 2147483000)); return; }
      if (left < -60000) { end(); return; }
      probing = true;
      try {
        const fresh = await apiRequest('/demo/state', { session });
        if (stopped) return;
        // (owner 2026-11-10) The server moves expires_at on each request (idle expiry): take the new end and wait again.
        if (Date.parse(fresh?.expires_at || '') > expires) {
          const moved = { ...session, expires_at: fresh.expires_at };
          if (sessionRef.current?.session_id === session.session_id) { sessionRef.current = moved; storeSession(moved); }
          setState((current) => (current && current.session_id === session.session_id ? { ...current, expires_at: fresh.expires_at } : current));
          return;
        }
        timer = window.setTimeout(check, 5000);
      } catch (failure) {
        if (stopped) return;
        if (failure.status === 401) end();
        else timer = window.setTimeout(check, Math.max(5000, retrySecondsLeft(failure) * 1000));
      } finally { probing = false; }
    };
    // A sleeping tab's timer can run late: check again when the tab comes back.
    const onVisible = () => { if (document.visibilityState === 'visible') check(); };
    check();
    document.addEventListener('visibilitychange', onVisible);
    window.addEventListener('focus', onVisible);
    return () => { stopped = true; window.clearTimeout(timer); document.removeEventListener('visibilitychange', onVisible); window.removeEventListener('focus', onVisible); };
  }, [state?.session_id, state?.expires_at, expireSession]); // eslint-disable-line react-hooks/exhaustive-deps

  const generateAiBrief = async (stage) => {
    if (aiControllerRef.current || busyRef.current || !sessionRef.current) return;
    invalidateAi();
    const controller = new AbortController();
    aiControllerRef.current = controller;
    const revision = aiRevisionRef.current;
    const identity = sessionRef.current.session_id;
    const session = sessionRef.current;
    const referenceRevision = referenceRevisionRef.current;
    setAiBusyStage(stage);
    setError(null);
    setNotice('');
    try {
      const body = stage === 'dispute_mediation' && caseItem?.case_ref ? { stage, case_ref: caseItem.case_ref } : { stage };
      const result = await apiRequest('/ai/evidence-brief', { method: 'POST', body, session, signal: controller.signal });
      if (!mounted.current || controller.signal.aborted || revision !== aiRevisionRef.current || sessionRef.current?.session_id !== identity) return;
      setAiBriefs({ [stage]: result });
    } catch (failure) {
      if (controller.signal.aborted || revision !== aiRevisionRef.current || sessionRef.current?.session_id !== identity) return;
      setAiBriefs({});
      if (failure.code === 'ai_disabled' || failure.code === 'ai_not_configured') { setAiNotices({ [stage]: AI_NOT_CONFIGURED_NOTICE }); return; }
      if (failure.code === 'hosted_demo_disabled') { setAiNotices({ [stage]: HOSTED_NOTES.ai }); return; }
      setError(failure);
      if (failure.status === 401) expireSession(failure, identity, referenceRevision);
    } finally {
      if (aiControllerRef.current === controller) aiControllerRef.current = null;
      if (mounted.current && revision === aiRevisionRef.current) setAiBusyStage('');
    }
  };

  const inject = (scenario, { automatic = false } = {}) => action(scenario, async (session) => {
    invalidateAi();
    const nextState = await apiRequest('/demo/inject', { method: 'POST', body: { scenario }, session });
    setState(nextState);
    if (scenario === 'reset') {
      setDraft(null); setReceipt(null); setSelectedCase(''); setReviewChecked(false);
      writeStored(RAN_STORE_KEY, null); writeStored(SENT_STORE_KEY, null); setClearedOnReload(false);
      setAup(null); setInvoiceReview(null); setInvoice(null); setInvoiceChecked(false);
      setVelocityQuickFilter(''); setSelectedVelocityTransaction(null);
      setEvidencePreview(null); setProviderDisputeDetail(null);
      // The server forgets the session's country check on reset; the panel and step status follow.
      setCountryCheck(null); setCountryStale(false); setCountryResetCount((count) => count + 1);
      setLastCountryCheck(null); setTrackingPreview(null);
      // (r34 #3) Reset demo clears the server's case <-> dispute pairings; the page forgets its copies too.
      sentReceipts.current = {}; boundByCaseRef.current = {}; sentByCaseRef.current = {}; setPreviewRefusal(null); setRestoredSend(null);
      // (r31 J5) Reset demo empties the review a confirmation was issued for; the console drops both kinds too.
      sendConfirmTokens.current.clearAll();
      autoLoadedRef.current = { burst: false, dispute: false };
    }
    // The spike chart starts below the fold at 1280x800 (UI/UX r16 P1): bring it into view once the sales load.
    // The result (the numbers and the alert line) is what comes into view, never the guide cards or the footer.
    if (scenario === 'burst' && !automatic) window.requestAnimationFrame(() => (document.querySelector('#velocity .velocity-metrics') || document.getElementById('velocity-pane-chart'))?.scrollIntoView({
      behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'center' }));
    setNotice(scenario === 'reset' ? 'Demo data reset; the session remains active.' : scenario === 'burst' ? 'Sample sales loaded.' : automatic ? '' : 'Scenario loaded. Loading it again will not duplicate records.');
  });

  const disabled = loading || Boolean(busy) || !state || error?.status === 401;
  const referenceProps = { session: state ? sessionRef.current : null, revision: referenceRevision, unavailable: disabled, onSessionExpired: expireSession };
  // (attack r23) An automatic stage load refused with Retry-After runs again when the step is opened after the wait.
  useEffect(() => {
    const scenario = activeStage === 'velocity' ? 'burst' : activeStage === 'disputes' ? 'dispute' : null;
    if (scenario && autoLoadedRef.current[scenario] === 'failed' && cooldownRef.current[scenario] && !coolingNow(scenario)) autoLoadedRef.current[scenario] = false;
  }, [activeStage]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => {
    // Entering a stage loads its synthetic scenario once, so no stage starts empty.
    if (!state || disabled) return;
    const scenario = activeStage === 'velocity' ? 'burst' : activeStage === 'disputes' ? 'dispute' : null;
    if (!scenario || state.scenario?.[scenario] || autoLoadedRef.current[scenario]) return;
    // Marked done only after the load worked (attack r21 desktop #17, phone #12): a failure is kept as 'failed' (no
    // retry loop while offline) and the 'online' listener below clears it, so the stage loads once the network is back.
    autoLoadedRef.current[scenario] = 'loading';
    inject(scenario, { automatic: true }).then((ok) => {
      if (autoLoadedRef.current[scenario] === 'loading') autoLoadedRef.current[scenario] = ok === true ? true : 'failed';
    });
  }, [activeStage, state, disabled, onlineCount]);
  useEffect(() => {
    const onOnline = () => {
      for (const key of Object.keys(autoLoadedRef.current)) if (autoLoadedRef.current[key] === 'failed') autoLoadedRef.current[key] = false;
      // No session yet (the page loaded offline): start one, as Reconnect would.
      // An expired session (401) keeps waiting for the seller's own Reconnect.
      if (!sessionRef.current && !busyRef.current && errorRef.current?.status !== 401) bootstrapRef.current?.();
      setOnlineCount((count) => count + 1);
    };
    window.addEventListener('online', onOnline);
    return () => window.removeEventListener('online', onOnline);
  }, []);
  useEffect(() => {
    // Stage 03 reads provider dispute records: Sandbox when connected, fixture otherwise.
    if (activeStage !== 'disputes' || !state || loading || !sessionRef.current) return;
    const session = sessionRef.current;
    const key = `${session.session_id}:${sandbox?.status || ''}`;
    if (providerDisputesKeyRef.current === key) return;
    providerDisputesKeyRef.current = key;
    apiRequest('/paypal/disputes', { session }).then((result) => {
      if (!mounted.current || sessionRef.current?.session_id !== session.session_id) return;
      setProviderDisputes(result); setProviderDisputeDetail(null); setEvidencePreview(null); setTrackingPreview(null);
    }).catch((failure) => {
      if (!mounted.current || sessionRef.current?.session_id !== session.session_id) return;
      setProviderDisputes({ error: failure.message });
    });
  }, [activeStage, state, loading, sandbox?.status]);
  // Hosted read-only Sandbox: refresh the dispute list every 60 s while the tab is visible and the Sandbox is connected.
  // Any error (a 429 read limit included) stops the timer and shows one "paused" notice; a new connect starts it again.
  useEffect(() => {
    if (!sandboxReads || activeStage !== 'disputes' || sandbox?.status !== 'connected' || !sessionRef.current) return undefined;
    const session = sessionRef.current;
    const timer = window.setInterval(() => {
      if (document.visibilityState !== 'visible' || !mounted.current || sessionRef.current?.session_id !== session.session_id) return;
      apiRequest('/paypal/disputes', { session }).then((result) => {
        if (!mounted.current || sessionRef.current?.session_id !== session.session_id) return;
        setProviderDisputes(result);
      }).catch(() => { window.clearInterval(timer); if (mounted.current) setNotice(HOSTED_NOTES.paused); });
    }, 60000);
    return () => window.clearInterval(timer);
  }, [sandboxReads, activeStage, sandbox?.status]);
  const loadProviderDispute = (disputeId) => action('provider-dispute', async (session) => {
    const result = await apiRequest(`/paypal/disputes/${disputeId}`, { session });
    // (fix r1 F1) A dispute this page sent evidence to shows its receipt again, with this fresh read as the read-back.
    // (round2 X, B 6a/6d) One kept only in this tab's storage (after a reload) gets the SUBMITTED stamp only when this
    // fresh read confirms it (restoredSendState); otherwise its note is shown without the stamp and it locks nothing.
    const mine = sentReceipts.current[disputeId] || null;
    const stored = mine ? null : readStoredReceipts(session.session_id)[disputeId] || null;
    const restored = restoredSendState(stored, result);
    const kept = mine || (restored?.confirmed ? stored : null);
    if (kept) { rememberBinding(kept.result); rememberSent(kept.result); }
    if (mine) rememberReceipt(session, mine.result, { status: result.status, debug: result.paypal_debug_id });
    setProviderDisputeDetail(result); setEvidencePreview(kept ? kept.result : null); setTrackingPreview(null); setPreviewRefusal(null);
    setRestoredSend(restored);
    if (kept) setSendReadback({ status: result.status, debug: result.paypal_debug_id });
  });
  const rememberReceipt = (session, result, readback) => {
    if (result?.external_send !== 'SUBMITTED') return;
    // (round2 X) Page memory holds only this page's own sends; rows read from storage are never copied into it.
    // (external review 2026-11-10 #6) The stored copy is merged with what this tab already stored: after a reload the
    // memory copy is empty, and writing it alone dropped the receipt of another dispute sent in the same session.
    const sentAt = sentReceipts.current[result.dispute_id]?.sent_at || new Date().toISOString();
    sentReceipts.current = { ...sentReceipts.current, [result.dispute_id]: { result, readback, sent_at: sentAt } };
    writeStored(SENT_STORE_KEY, { session_id: session.session_id, items: { ...readStoredReceipts(session.session_id), ...sentReceipts.current } });
  };
  // (r34 #7) A refused preview (409: wrong reason or amount, case already paired, PayPal already has evidence) is not
  // a failure toast: its sentence becomes the lock line under Submit and the hold line in the send guard, in place,
  // so on a phone nothing covers the sticky bar. Every other failure goes to the usual error banner.
  const requestPreview = async (kind, session) => {
    const request = { dispute_id: providerDisputeDetail.dispute_id, case_ref: caseItem.case_ref };
    setPreviewRefusal(null);
    try {
      return await apiRequest(kind === 'tracking' ? '/paypal/disputes/add-tracking' : '/paypal/disputes/provide-evidence', { method: 'POST', body: { ...request, submit: false }, session });
    } catch (failure) {
      if (failure?.status !== 409) throw failure;
      setPreviewRefusal({ kind, ...request, message: failure.message || 'The server refused this preview. Nothing was sent.' });
      return null;
    }
  };
  const previewEvidence = () => action('evidence-preview', async (session) => {
    if (sellerEvidenceOnFile(providerDisputeDetail)) return;
    if (evidencePreview?.external_send === 'SUBMITTED') return; // (fix r1 F2) this session's send for the open dispute stays on screen
    const result = await requestPreview('evidence', session);
    if (!result) return;
    rememberBinding(result);
    setEvidencePreview(result);
  });
  const submitEvidence = () => action('evidence-submit', async (session) => {
    const result = await apiRequest('/paypal/disputes/provide-evidence', { method: 'POST', body: sendConfirmTokens.current.submitBody('evidence', { dispute_id: providerDisputeDetail.dispute_id, case_ref: caseItem.case_ref }), session });
    setSendReadback(null); setRestoredSend(null);
    rememberSent(result);
    rememberReceipt(session, result, null);
    setEvidencePreview(result);
    setNotice('Evidence request submitted to the PayPal Sandbox after local approval.');
    // (UX round 2) The result is the point of the step: bring the SUBMITTED card to the middle of the screen.
    setTimeout(() => document.querySelector('[data-testid="send-receipt"]')?.scrollIntoView({ block: 'center' }), 400);
    // Read-back: the dispute as PayPal now reports it (one GET), and on the hosted demo the caps left.
    if (result?.external_send === 'SUBMITTED') {
      apiRequest(`/paypal/disputes/${result.dispute_id}`, { session }).then((fresh) => { setSendReadback({ status: fresh.status, debug: fresh.paypal_debug_id }); rememberReceipt(session, result, { status: fresh.status, debug: fresh.paypal_debug_id });
        // (fix r1 F2b) The open detail shows what PayPal reports now, not the status from before the send.
        setProviderDisputeDetail((current) => (current?.dispute_id === fresh.dispute_id ? fresh : current)); setProviderDisputes((list) => (list?.items ? { ...list, items: list.items.map((row) => (row.dispute_id === fresh.dispute_id ? { ...row, status: fresh.status } : row)) } : list)); }).catch(() => setSendReadback({ status: null }));
      if (sandboxSend) apiRequest('/connections', { session }).then((next) => setSendState(next?.send_state || null)).catch(() => {});
    }
  });
  // (optimise r24) Tracking preview is always allowed; the send needs the same gates as evidence (recorded local review,
  // Sandbox source, server flag PAYGUARD_PAYPAL_TRACKING_SUBMIT on, preview frozen). Checks never click the send.
  const previewTracking = () => action('tracking-preview', async (session) => {
    const result = await requestPreview('tracking', session);
    if (!result) return;
    rememberBinding(result);
    setTrackingPreview(result);
  });
  const submitTracking = () => action('tracking-submit', async (session) => {
    const result = await apiRequest('/paypal/disputes/add-tracking', { method: 'POST', body: sendConfirmTokens.current.submitBody('tracking', { dispute_id: providerDisputeDetail.dispute_id, case_ref: caseItem.case_ref }), session });
    rememberSent(result);
    setTrackingPreview(result);
    setNotice('Tracking sent to the PayPal Sandbox after local approval.');
  });
  // Declared before the send guard below reads it.
  const caseItem = state?.disputes?.find((item) => item.case_ref === selectedCase) || state?.disputes?.[0];
  // (round2 X, B 2c/5a) The pairing and sent keys are the full dispute id the API returned for that preview or send (the
  // hosted code, or the raw local id). The server's short form (bound_dispute_masked, "PP-R-…01") only says a pairing
  // exists; two disputes can share it, so it is never stored or compared as an identity.
  const rememberBinding = (result) => {
    if (result?.send_guard?.bound_dispute_masked && typeof result.dispute_id === 'string') boundByCaseRef.current[result.case_ref] = result.dispute_id;
  };
  const rememberSent = (result) => {
    if (result?.external_send === 'SUBMITTED' && typeof result.dispute_id === 'string') sentByCaseRef.current[result.case_ref] = result.dispute_id;
  };
  const boundTo = caseItem ? boundByCaseRef.current[caseItem.case_ref] || null : null;
  const sentTo = caseItem ? sentByCaseRef.current[caseItem.case_ref] || null : null;
  const sentToShown = sentTo ? displayDisputeId(sentTo) : null;
  const sellerEvidence = sellerEvidenceOnFile(providerDisputeDetail);
  // (fix r1 F2) Evidence for the open dispute went out in this session: its receipt stays and no new preview replaces it.
  const evidenceSent = evidencePreview?.external_send === 'SUBMITTED';
  // (round2 X) The SUBMITTED card on screen came from this tab's storage and the fresh read-back confirmed it.
  const keptReceipt = Boolean(evidenceSent && restoredSend?.confirmed && restoredSend.dispute_id === evidencePreview?.dispute_id);
  // Only the refusal for the dispute and case now on screen counts.
  const refusalFor = (kind) => (previewRefusal && previewRefusal.kind === kind && previewRefusal.dispute_id === providerDisputeDetail?.dispute_id
    && previewRefusal.case_ref === caseItem?.case_ref ? previewRefusal.message : null);
  const evidenceRefusal = refusalFor('evidence');
  const trackingRefusal = refusalFor('tracking');
  const evidenceBlock = sendGuardBlock(evidencePreview?.send_guard, providerDisputeDetail, caseItem, boundTo, sentTo, evidencePreview?.dispute_id);
  const trackingBlock = sendGuardBlock(trackingPreview?.send_guard, providerDisputeDetail, caseItem, boundTo, sentTo, trackingPreview?.dispute_id);
  // Before step 2 enables: a fresh preview must carry the same payload_sha256 and still pass every check above.
  const recheckSend = async (kind) => {
    const session = sessionRef.current;
    const before = kind === 'tracking' ? trackingPreview : evidencePreview;
    // (r31 J5) Only the latest re-check's token may go out: a failed re-check leaves none.
    sendConfirmTokens.current.clear(kind);
    try {
      const fresh = await apiRequest(kind === 'tracking' ? '/paypal/disputes/add-tracking' : '/paypal/disputes/provide-evidence',
        { method: 'POST', body: { dispute_id: providerDisputeDetail.dispute_id, case_ref: caseItem.case_ref, submit: false }, session });
      const held = sendGuardBlock(fresh.send_guard, providerDisputeDetail, caseItem, boundTo, sentTo, fresh.dispute_id);
      if (!before?.payload_sha256 || fresh.payload_sha256 !== before.payload_sha256 || held) {
        setSendConfirm(null);
        setNotice(held || 'What would be sent changed since the preview; nothing was sent. Prepare the preview again.');
        return false;
      }
      // (r32 J5 P3-1) Ready but no token: the send would only end in 409, so no countdown.
      if (readyWithoutToken(fresh)) {
        setSendConfirm(null);
        setNotice(MISSING_CONFIRM_NOTICE);
        return false;
      }
      sendConfirmTokens.current.remember(kind, fresh);
      return true;
    } catch (failure) {
      setSendConfirm(null);
      setError(failure);
      return false;
    }
  };
  const confirmSend = async (kind) => {
    setSendConfirm(null);
    await (kind === 'tracking' ? submitTracking() : submitEvidence());
    sendConfirmTokens.current.clear(kind);
  };
  // (2026-11-10) A review the server recorded before a reload counts like this page's own receipt for the sends; the
  // server still checks the approval and the single-use confirmation, so this only stops a resumed page locking itself.
  const reviewRecorded = Boolean(receipt) || (caseItem?.status === 'local_draft_reviewed' && draft?.case_ref === caseItem?.case_ref);
  const trackingSubmitReady = reviewRecorded && trackingPreview?.submit_flag_enabled === true && trackingPreview?.source === 'paypal_sandbox' && trackingPreview?.external_send === 'FROZEN' && !trackingBlock;
  const itemNotReceived = providerDisputeDetail?.reason === 'MERCHANDISE_OR_SERVICE_NOT_RECEIVED';
  // (2026-11-10) Hosted send: nothing left when no listed Sandbox dispute waits for the seller, or the shared cap is used.
  const sendCapped = sandboxSend && Boolean(sendState) && (sendState.sends_left_day === 0 || sendState.sends_left_window === 0);
  const sendNoneLeft = sandboxSend && evidencePreview?.external_send !== 'SUBMITTED' && (sendCapped || (providerDisputes?.source === 'paypal_sandbox'
    && !(providerDisputes.items || []).some((row) => row.status === 'WAITING_FOR_SELLER_RESPONSE')));
  const evidenceSubmitReady = reviewRecorded && evidencePreview?.submit_flag_enabled === true && evidencePreview?.source === 'paypal_sandbox' && evidencePreview?.external_send === 'FROZEN' && !evidenceBlock && !sellerEvidence;
  // (r31 A4) The visible line under each locked send, from the same inputs as the two Ready flags above.
  const sessionExpired = error?.status === 401;
  const evidenceLock = sendLockReason({ kind: 'evidence', sessionExpired, draft, receipt: reviewRecorded ? (receipt || { restored: true }) : null, preview: evidencePreview, block: evidenceBlock, disputeSelected: Boolean(providerDisputeDetail), sellerEvidence, refusal: evidenceRefusal });
  const trackingLock = sendLockReason({ kind: 'tracking', sessionExpired, draft, receipt: reviewRecorded ? (receipt || { restored: true }) : null, preview: trackingPreview, block: trackingBlock, disputeSelected: Boolean(providerDisputeDetail), refusal: trackingRefusal });
  // (r32 J4 P1-2, J1) One obvious primary per step: a send that is ready is the solid blue button without a lock icon;
  // when the evidence send is ready it is the next step and a ready tracking send stays secondary beside it.
  const trackingSendTone = !trackingSubmitReady ? 'ghost' : evidenceSubmitReady ? 'secondary' : 'blue';
  const velocity = state?.velocity;
  const chartVelocity = useMemo(() => phoneChartVelocity(velocity, narrowScreen), [velocity, narrowScreen]);
  // A review the server records for this case while this page has no receipt for it (a resumed session, attack r23).
  const reviewedOnServer = !receipt && caseItem?.status === 'local_draft_reviewed';
  // Closed by default (plan r2 A3): the case queue already lists every case; the board is one click away.
  const boardOpen = boardExpanded ?? false;
  const boardDraftsForState = useMemo(() => (boardDrafts.session && boardDrafts.session === state?.session_id ? boardDrafts.drafts : {}), [boardDrafts, state?.session_id]);
  // One status per step on the step navigator, so a reviewer sees what is done, current or still empty.
  const stepStatus = {
    // Either check in step 01 counts: the country rules result or the description check (review r1 P0.6).
    compliance: aupPhase === 'loading' ? { label: 'Checking', tone: 'blue' }
      : countryHeld ? { label: 'No draft: a rule stops it', tone: 'danger' }
      : aup?.findings?.length ? { label: 'Needs review', tone: 'amber' }
      : aup || countryCheck ? { label: 'Checked', tone: 'green' } : { label: 'Not started', tone: 'muted' },
    velocity: !velocity || !velocity.transaction_count ? { label: 'No sales loaded', tone: 'muted' }
      : velocity.alert ? { label: 'Needs review', tone: 'amber' } : { label: 'Within usual range', tone: 'green' },
    disputes: receipt || reviewedOnServer ? { label: 'Review recorded', tone: 'green' } : draft ? { label: 'Draft ready', tone: 'blue' }
      : state?.disputes?.length ? { label: 'Case loaded', tone: 'amber' } : { label: 'No case loaded', tone: 'muted' },
  };
  useEffect(() => {
    if (!selectedVelocityTransaction) return;
    const current = state?.transactions?.find((transaction) => transaction.order_id === selectedVelocityTransaction.order_id);
    if (!current) {
      setSelectedVelocityTransaction(null);
      setVelocityQuickFilter('');
    } else if (current !== selectedVelocityTransaction) {
      setSelectedVelocityTransaction(current);
    }
  }, [selectedVelocityTransaction, state?.transactions]);
  // (fix r1 F5) getRowClass only runs when a row is drawn: redraw on a new selection so the old row drops its marker.
  const velocityGridApi = useRef(null);
  const selectedOrderId = selectedVelocityTransaction?.order_id || '';
  useEffect(() => { try { velocityGridApi.current?.redrawRows(); } catch { /* grid already gone */ } }, [selectedOrderId]);
  const columns = useMemo(() => [
    { field: 'order_id', headerName: 'ORDER ID', minWidth: 190, flex: 1.4, cellRenderer: ({ value }) => <span className="grid-order"><span className="tiny-dot" />{value}</span> },
    { field: 'amount', headerName: 'AMOUNT', minWidth: 120, flex: 1, cellClass: 'grid-amount', valueFormatter: ({ value }) => value ?? '—' },
    { field: 'currency', headerName: 'CURRENCY', headerTooltip: 'Currency', minWidth: 132, flex: 0.8 },
    // (fix r1 F3, F4) The cell shows the viewer's clock time (dateLabel) while the value is a UTC timestamp: both the quick filter and
    // the column's own filter match the text on screen (the raw timestamp still matches the quick filter), and the
    // column is declared as text so its filter icon opens the same text popup as the other columns.
    { field: 'occurred_at', headerName: 'CAPTURED AT', minWidth: 180, flex: 1.2, cellDataType: 'text', filter: 'agTextColumnFilter', valueFormatter: ({ value }) => dateLabel(value),
      filterValueGetter: ({ data }) => dateLabel(data?.occurred_at), getQuickFilterText: ({ value }) => `${dateLabel(value)} ${value || ''}` },
  ], []);

  // Optional Channel3 category signal: runs after the rule result is shown and never changes it.
  const lookupCategory = (session, evaluationId, text, revision) => {
    const controller = new AbortController();
    categoryControllerRef.current = controller;
    setCategorySignal({ status: 'LOADING' });
    const current = () => mounted.current && !controller.signal.aborted && revision === aupRevisionRef.current && sessionRef.current === session;
    apiRequest('/aup/category-signal', { method: 'POST', body: { evaluation_id: evaluationId, description: text }, session, signal: controller.signal })
      .then((result) => { if (current()) setCategorySignal(result); })
      .catch(() => { if (current()) setCategorySignal({ status: 'UNAVAILABLE' }); });
    // Channel3 product reference cards, on the same controller: the seller confirms which one is theirs.
    setProductRef({ status: 'LOADING' });
    apiRequest('/aup/product-reference', { method: 'POST', body: { evaluation_id: evaluationId, description: text }, session, signal: controller.signal })
      .then((result) => { if (current()) setProductRef(result); })
      .catch(() => { if (current()) setProductRef({ status: 'UNAVAILABLE' }); })
      .finally(() => { if (categoryControllerRef.current === controller) categoryControllerRef.current = null; });
  };
  const confirmProduct = (productId) => action('product', async (session) => {
    // Guarded by the confirmation revision and the session it was requested in: an edit, a new check or a new
    // session while the request is in flight drops the reply instead of attaching a card to the wrong text.
    const requested = { revision: productConfirmationRef.current.revision, session: session.session_id };
    const result = await apiRequest('/aup/product-reference/confirm', { method: 'POST', session,
      body: { evaluation_id: aup.evaluation_id, description, product_id: productId } });
    const current = productConfirmationRef.current;
    if (!mounted.current || current.revision !== requested.revision || current.session !== requested.session || sessionRef.current !== session) return;
    dispatchProductConfirmation({ type: 'confirmed', record: result, ...requested });
    setNotice(result.choice === 'CONFIRMED' ? 'Product confirmed by you; it will be added to the review ZIP.' : 'Recorded: none of the catalogue products is yours.');
  });
  // Field messages from the client-side checks (attack r21): shown under the field, nothing is sent.
  // The description note is live (it shows as soon as the text is over the limit); the amount note shows on Confirm.
  const [amountNote, setAmountNote] = useState('');
  // Run Policy Check buttons go through this guard; scan() is the request itself.
  // attack r22: one request at a time and no repeat while a result for this exact text is on screen. Under CPU
  // throttling six clicks sent three checks in a row, and three taps on the phone bar used the 5-per-2-minute budget
  // and turned the result into "Check incomplete". An edit, expiry, Cancel or Return to edit clears `aup`, so a new
  // check is always one edit away; after Confirm Draft Context (aupConsumed) a re-run stays possible as before.
  // (r32 J4 P1-1) When the shown result arrived (epoch ms), for the re-press rule below.
  const aupCheckedAtRef = useRef(0);
  const runPolicyCheck = () => {
    if (busyRef.current) return;
    aupAutoRenewsRef.current = 0;
    if (descriptionProblem(description)) {
      afterRender(() => document.getElementById('description-note')?.scrollIntoView({ block: 'center' }));
      return;
    }
    if (coolingNow('aup')) return;
    if (aup && !aupConsumed) {
      // (r32 J4 P1-1) A deliberate press 30 s or more after the shown check runs it again, so the 2-minute window starts
      // over (the server has no endpoint that extends an evaluation). A burst of taps inside 30 s still sends nothing.
      if (Date.now() - aupCheckedAtRef.current >= AUP_RENEW_AFTER_MS) { scan(); return; }
      // Neutral and lasting (attack r23): it stays until the description changes, not a green toast that fades.
      setNotice(''); setInfo({ kind: 'already', text: 'Already checked. To restart the 2-minute window, press Run Policy Check again 30 seconds after a check.' });
      afterRender(() => document.querySelector('[data-testid="aup-result"]')?.scrollIntoView({ block: 'nearest' }));
      return;
    }
    scan();
  };
  // (optimise r24) The text the shown policy result was checked for; "Keep this result" re-runs only when it still matches.
  const aupCheckedTextRef = useRef('');
  const keepAupResult = () => {
    if (!aup || busyRef.current || coolingNow('aup')) return;
    if (aupCheckedTextRef.current !== description) {
      setInfo({ kind: 'already', text: 'The description changed after this check. Run Policy Check again.' });
      return;
    }
    scan();
  };
  const scan = () => action('aup', async (session) => {
    invalidateAup();
    dispatchProductConfirmation({ type: 'clear', reason: 'policy_check' });
    // (owner 2026-11-10) Set only by the automatic renewal, for this one run.
    const quiet = aupQuietRef.current;
    aupQuietRef.current = false;
    const revision = aupRevisionRef.current;
    const controller = new AbortController();
    aupControllerRef.current = controller;
    setAupPhase('loading');
    try {
      const result = await apiRequest('/aup/review', { method: 'POST', body: { description }, session, signal: controller.signal });
      if (!mounted.current || controller.signal.aborted || revision !== aupRevisionRef.current || sessionRef.current !== session) return;
      writeStored(RAN_STORE_KEY, { ran: true });
      setAup(result); setAupPhase('completed'); aupCheckedTextRef.current = description; aupCheckedAtRef.current = Date.now();
      // Bring the result above the phone action bar (scroll-margin-bottom in index.css; attack r21 phone #6).
      // An automatic renewal (quiet) leaves the page where the seller is reading.
      if (!quiet) window.requestAnimationFrame(() => document.querySelector('[data-testid="aup-result"]')?.scrollIntoView({
        block: 'nearest', behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' }));
      lookupCategory(session, result.evaluation_id, description, revision);
    } catch (failure) {
      if (!controller.signal.aborted && revision === aupRevisionRef.current) setAupPhase('error');
      throw failure;
    } finally { if (aupControllerRef.current === controller) aupControllerRef.current = null; }
  });
  // (owner 2026-11-10) An unreviewed dispute draft is prepared again just after its 5-minute window (see draftAutoRef).
  useEffect(() => {
    if (!draft || receipt) return undefined;
    const caseRef = draft.case_ref;
    const timer = setTimeout(() => {
      const auto = draftAutoRef.current;
      if (!auto?.canRenew(caseRef)) return;
      draftAutoRenewsRef.current += 1;
      draftQuietRef.current = true;
      auto.getDraft().finally(() => { draftQuietRef.current = false; });
    }, DRAFT_AUTO_RENEW_AFTER_MS);
    return () => clearTimeout(timer);
  }, [draft, receipt]);
  draftAutoRef.current = {
    // A call-time lookup: getDraft is declared further down in this render.
    getDraft: () => getDraft(),
    canRenew: (caseRef) => Boolean(draft) && draft.case_ref === caseRef && caseItem?.case_ref === caseRef && !busyRef.current &&
      !receipt && !reviewedOnServer && Boolean(sessionRef.current) && !coolingNow('draft') &&
      document.visibilityState === 'visible' && draftAutoRenewsRef.current < DRAFT_AUTO_RENEW_LIMIT,
  };
  aupAutoRef.current = {
    scan,
    canRenew: () => Boolean(aup) && !busyRef.current && !aupConsumed && !productConfirm && !draftConfirmRef.current &&
      Boolean(sessionRef.current) && aupCheckedTextRef.current === description && !coolingNow('aup') &&
      document.visibilityState === 'visible' && aupAutoRenewsRef.current < AUP_AUTO_RENEW_LIMIT,
  };
  const getDraft = () => action('draft', async (session) => {
    invalidateAi();
    const quiet = draftQuietRef.current;
    draftQuietRef.current = false;
    if (!quiet) draftAutoRenewsRef.current = 0;
    const result = await apiRequest(`/disputes/${encodeURIComponent(caseItem.case_ref)}/draft`, { method: 'POST', body: {}, session });
    setSelectedCase(caseItem.case_ref); setDraft(result); setReceipt(null);
    // An automatic renewal keeps the seller's tick and place on the page; only the 5-minute window starts over.
    if (!quiet) setReviewChecked(false);
    setState(await apiRequest('/demo/state', { session }));
    if (quiet) { setInfo({ kind: 'resumed', text: DRAFT_RENEWED_TEXT }); return; }
    setNotice('Draft ready. Review it below.');
    window.setTimeout(() => document.querySelector('[data-testid="dispute-route"]')?.scrollIntoView({ block: 'start', behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' }), 80);
  });
  const approve = () => action('approve', async (session) => {
    const result = await apiRequest(`/disputes/${encodeURIComponent(draft.case_ref)}/approve`, { method: 'POST', body: { draft_digest: draft.draft_digest }, session });
    setReceipt(result);
    setState(await apiRequest('/demo/state', { session }));
    setNotice('Local draft review recorded.'); // (fix r1 U9) the receipt line beside it already says "Not submitted"
    // (UX round 1) The next action is in the PayPal disputes section below: open it, so the step is on screen.
    { const next = document.querySelector('[data-testid="provider-disputes"]'); if (next) next.open = true; }
    // The confirm button is now disabled; focus moves to the recorded receipt instead of the page (click-all #5).
    // It waits until the action ends: the button only turns disabled then, which dropped focus to BODY (attack r21
    // desktop #5); the receipt is scrolled to the middle so the success toast does not cover it (phone #9).
    focusWhenIdle(['[data-testid="dispute-result"]'], { scroll: true });
  });
  // One file per click burst (attack r21 desktop #12).
  const downloadAtRef = useRef({});
  const firstClick = (key) => {
    const now = Date.now();
    if (now - (downloadAtRef.current[key] || 0) < DOWNLOAD_REPEAT_MS) return false;
    downloadAtRef.current[key] = now;
    return true;
  };
  const downloadRedactedFile = () => {
    if (!firstClick('redacted')) return;
    try {
      downloadPseudonymizedEvidence(draft?.document_redaction);
      setError(null);
      setNotice('Evidence file with personal details replaced was saved on this computer; nothing was sent to PayPal.');
    } catch {
      setNotice('');
      setError({ status: 422, code: 'pseudonymized_export_invalid', message: 'The evidence file could not be created from this draft.' });
    }
  };
  const downloadReviewZip = () => {
    if (!firstClick('zip')) return;
    try {
      downloadInternalReviewZip(draft, productConfirm);
      setError(null);
      setNotice('Internal review ZIP downloaded locally. It is not a PayPal evidence attachment, is not complete official evidence, and was not submitted. Verify the live dispute response and original evidence before any external use.');
    } catch {
      setNotice('');
      setError({ status: 422, code: 'internal_review_zip_invalid', message: 'Internal Review ZIP creation failed. No file was downloaded or submitted to PayPal.' });
    }
  };
  const bindInvoice = async (session, evaluation, acknowledgementToken, revision, signal) => {
    const result = await apiRequest('/paypal/invoices/review', { method: 'POST', body: {
      description, amount: invoiceAmountValue(invoiceAmount), currency: 'USD', confirm_sandbox_draft: true,
      evaluation_id: evaluation.evaluation_id, description_digest: evaluation.description_digest,
      acknowledgement_token: acknowledgementToken,
    }, session, signal });
    if (!mounted.current || signal.aborted || revision !== aupRevisionRef.current || sessionRef.current !== session) return;
    setInvoiceReview(result); setInvoice(null); setAupConsumed(true); setWarningOpen(false);
    // Keyboard Enter left focus on BODY once the button turned disabled (attack r23): go to the draft step's next control.
    focusWhenIdle(AFTER_DRAFT_CONTEXT, { scroll: 'fallback' });
  };
  // A server answer about the amount alone keeps the policy result: only the amount needs fixing (attack r21 #7).
  const keepsPolicyResult = (failure) => failure?.code === 'invalid_amount' || (failure?.status === 422 && /amount/i.test(`${failure?.code || ''} ${failure?.message || ''}`));
  const reviewInvoice = () => {
    if (!aup || aupConsumed || busyRef.current) return;
    // Checked before anything is sent or the reminder opens: -5, abc, 1e309, 10.001 and 45.6.7 never reach the server.
    const amountProblem = invoiceAmountProblem(invoiceAmount);
    // attack r22 phone #6: the message is scrolled into view; on a touch screen the field is not focused, because the
    // keyboard it opens covered half of the message.
    if (amountProblem) { setAmountNote(amountProblem); afterRender(() => {
      if (!coarsePointer()) document.getElementById('invoice-amount')?.focus({ preventScroll: true });
      document.getElementById('invoice-amount-note')?.scrollIntoView({ block: 'center' });
    }); return; }
    if (descriptionProblem(description)) return;
    if (aup.match_status === 'REVIEW_SIGNAL') { setWarningOpen(true); return; }
    return action('invoice-review', async (session) => {
      const revision = aupRevisionRef.current;
      const controller = new AbortController(); aupControllerRef.current = controller;
      try { await bindInvoice(session, aup, null, revision, controller.signal); }
      catch (failure) { if (!controller.signal.aborted && revision === aupRevisionRef.current && !keepsPolicyResult(failure)) invalidateAup(); throw failure; }
      finally { if (aupControllerRef.current === controller) aupControllerRef.current = null; }
    });
  };
  const chooseWarning = (choice) => action('aup-choice', async (session) => {
    const evaluation = aup;
    if (!evaluation || !warningOpen) return;
    warningCloseRef.current = choice;
    const revision = aupRevisionRef.current;
    const controller = new AbortController(); aupControllerRef.current = controller;
    try {
      const result = await apiRequest('/aup/acknowledge', { method: 'POST', body: {
        evaluation_id: evaluation.evaluation_id, description_digest: evaluation.description_digest, choice,
      }, session, signal: controller.signal });
      if (!mounted.current || controller.signal.aborted || revision !== aupRevisionRef.current || sessionRef.current !== session) return;
      if (choice === 'ACKNOWLEDGE_AND_CONTINUE') {
        await bindInvoice(session, evaluation, result.acknowledgement_token, revision, controller.signal);
      } else {
        invalidateAup();
        setNotice(choice === 'RETURN_TO_EDIT' ? 'Returned to editing. Recheck the description after changes.' : 'Draft flow canceled. Recheck the description before continuing again.');
      }
    } catch (failure) {
      if (!controller.signal.aborted && revision === aupRevisionRef.current) invalidateAup();
      if (choice === 'ACKNOWLEDGE_AND_CONTINUE') focusWhenIdle(['[data-testid="aup-review"]', '[data-testid="phone-action-aup"]', '#stage-trigger-compliance']);
      throw failure;
    }
    finally { if (aupControllerRef.current === controller) aupControllerRef.current = null; }
  });
  const chooseWarningRef = useRef(chooseWarning);
  chooseWarningRef.current = chooseWarning;
  useEffect(() => {
    if (!warningOpen) return undefined;
    const onKey = (event) => {
      if (event.key !== 'Escape') return;
      event.preventDefault();
      if (!busyRef.current) chooseWarningRef.current('CANCEL');
    };
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, [warningOpen]);
  // A click on the backdrop keeps focus inside the dialog instead of dropping it to the page.
  const holdWarningFocus = (event) => {
    if (event.target !== event.currentTarget) return;
    event.preventDefault();
    warningRef.current?.focus({ preventScroll: true });
  };
  // Escape is handled on the document (above), so it still works after a click on the backdrop moved focus off the
  // dialog (attack r21 desktop #13).
  const warningKeys = (event) => {
    if (event.key !== 'Tab') return;
    const controls = [...warningRef.current.querySelectorAll('a[href],button:not(:disabled)')];
    if (!controls.length) { event.preventDefault(); return; }
    const first = controls[0], last = controls[controls.length - 1];
    if (event.shiftKey && (document.activeElement === first || !controls.includes(document.activeElement))) { event.preventDefault(); last.focus(); }
    else if (!event.shiftKey && (document.activeElement === last || !controls.includes(document.activeElement))) { event.preventDefault(); first.focus(); }
  };
  const connectSandbox = () => action('connect', async (session) => {
    setSandbox(null);
    try {
      const result = await apiRequest('/paypal/connect', { method: 'POST', body: {}, session });
      setSandbox(result);
      setNotice(result.evidence_receipt?.evidence_class === 'AUTHENTIC_SANDBOX_RESPONSE'
        ? 'Live Sandbox connection verified · credentials stay hidden.'
        : 'Demo test response · not a live Sandbox check; credentials stay hidden.');
    } catch (failure) {
      try { setSandbox(await apiRequest('/paypal/status', { session })); }
      catch { setSandbox(null); }
      throw failure;
    }
  });
  // (red team r26 #3 P1) The draft dialog closes when its basis goes: the 120 s policy result, the session, the
  // country stop or the Sandbox connection. createInvoice also refuses without a review.
  // (r31 J4 P1-2) Except the policy result's own expiry: the dialog then stays open with DRAFT_EXPIRED_TEXT and only
  // Back, so the seller sees why instead of a dialog that vanished and a cleared tick.
  useEffect(() => {
    if (draftConfirm && ((!invoiceReview && !draftExpired) || disabled || countryHeld || sandbox?.status !== 'connected')) setDraftConfirm(false);
  }, [draftConfirm, draftExpired, invoiceReview, disabled, countryHeld, sandbox?.status]);
  useEffect(() => { if (!draftConfirm) setDraftExpired(false); }, [draftConfirm]);
  const createInvoice = () => action('invoice', async (session) => {
    if (!invoiceReview) return;
    const result = await apiRequest('/paypal/invoices/draft', { method: 'POST', body: { description, amount: invoiceAmountValue(invoiceAmount), currency: 'USD', review_token: invoiceReview.review_token, payload_digest: invoiceReview.payload_digest }, session });
    setInvoice(result); setInvoiceReview(null); setInvoiceChecked(false);
    setNotice(`Sandbox invoice draft created; ${sandboxReadbackLabel(result.evidence_receipt?.separate_get_readback).toLowerCase()}, and nothing was sent.`);
  });

  // (fix r1 U8) Opens the PayPal disputes fold and brings its list to the top of the screen.
  const showProviderDisputes = () => {
    const fold = document.querySelector('[data-testid="provider-disputes"]');
    if (!fold) return;
    fold.open = true;
    fold.scrollIntoView({ block: 'start', behavior: 'auto' });
  };
  const reviewDone = Boolean(receipt) || reviewedOnServer;
  // Phones (<=640px): the current step's one primary action, repeated in a sticky bottom bar. Same handlers and
  // disabled rules as the in-page buttons; hidden by CSS on wider screens.
  // Country rules in view: the bar runs that check instead (the panel owns its own request and busy state).
  const phoneAction = activeStage === 'compliance'
    ? (phoneSection === 'country'
      // After a check that stops nothing, the bar offers the next step (red team 2026-11-03 P2-9).
      ? (countryCheck && !countryHeld
        ? { key: 'country-next', label: hasPostalBan(countryCheck) ? 'Continue with another carrier' : 'Continue to draft', icon: 'arrow', onClick: continueToDraft, disabled: !state }
        : { key: 'country', label: 'Check country rules', icon: 'shield', onClick: () => document.querySelector('[data-testid="country-check"]')?.click(), disabled: !state, loading: countryBusy })
      // After Confirm Draft Context the bar offers the draft step's own action, not Run Policy Check, which would drop
      // the bound draft context (attack r22 phone #10). The hosted demo has no draft action, so the bar steps aside.
      : invoiceReview ? (hosted ? null : sandbox?.status === 'connected'
        ? { key: 'invoice', label: 'Create Sandbox draft', icon: 'file', onClick: () => setDraftConfirm(true), disabled: disabled || countryHeld || !invoiceReview || !invoiceChecked, loading: busy === 'invoice', waiting: waitLeft('invoice') > 0 }
        : { key: 'connect', label: 'Connect US Sandbox', icon: 'link', onClick: connectSandbox, disabled, loading: busy === 'connect', waiting: waitLeft('connect') > 0 })
      : invoice ? null
      : { key: 'aup', label: 'Run Policy Check', icon: 'shield', onClick: runPolicyCheck, disabled: disabled || !description.trim(), blocked: Boolean(descriptionProblem(description)), loading: busy === 'aup', waiting: waitLeft('aup') > 0 })
    : activeStage === 'velocity'
      ? (velocity?.transaction_count ? null : { key: 'burst', label: 'Load sales burst', icon: 'bolt', onClick: () => inject('burst'), disabled, loading: busy === 'burst', waiting: waitLeft('burst') > 0 })
      : activeStage === 'disputes'
        // (r32 J4 P1-2) After the local review the bar shows the real next step: the preview, then the ready send.
        ? (reviewRecorded && (!hosted || sandboxSend) && evidenceSubmitReady
          ? { key: 'evidence-submit', label: 'Submit to PayPal Sandbox (test)', icon: 'arrow', onClick: () => setSendConfirm('evidence'), disabled: disabled || !evidenceSubmitReady, loading: busy === 'evidence-submit' }
          : reviewRecorded && !hosted && trackingSubmitReady
            ? { key: 'tracking-submit', label: 'Send tracking to PayPal Sandbox (test)', icon: 'arrow', onClick: () => setSendConfirm('tracking'), disabled: disabled || !trackingSubmitReady, loading: busy === 'tracking-submit' }
          // (fix r1 U8) With the review recorded the bar never shows a dead "Local review recorded": it offers the next
          // step that can be taken (connect the Sandbox, pick a dispute, then the preview below) and steps aside once
          // nothing is left (evidence sent, a held preview, the hosted demo without sends) and on the deadline board tab.
          : boardOpen || (reviewDone && (evidencePreview || (hosted && !sandboxSend))) ? null
          : reviewDone && sandboxReads && sandbox?.status !== 'connected'
            ? { key: 'connect-disputes', label: 'Connect US Sandbox', icon: 'link', onClick: () => { showProviderDisputes(); connectSandbox(); }, disabled, loading: busy === 'connect', waiting: waitLeft('connect') > 0 }
          : reviewDone && (providerDisputes?.items || []).length > 0 && (!providerDisputeDetail || sellerEvidence)
            ? { key: 'pick-dispute', label: providerDisputeDetail ? 'Pick another PayPal dispute' : 'Pick a PayPal dispute', icon: 'arrow', onClick: showProviderDisputes, disabled }
          : receipt && (!hosted || sandboxSend) && providerDisputeDetail && !evidencePreview
            ? { key: 'evidence-preview', label: 'Prepare evidence request (preview)', icon: 'file', onClick: previewEvidence, disabled: disabled || !draft || !providerDisputeDetail || sellerEvidence, loading: busy === 'evidence-preview' }
          : reviewDone ? null
          : !draft
          ? { key: 'draft', label: 'Prepare evidence draft', icon: 'file', onClick: getDraft, disabled: disabled || !caseItem || caseItem.status === 'local_draft_reviewed', loading: busy === 'draft', waiting: waitLeft('draft') > 0 }
          : { key: 'approve', label: receipt || reviewedOnServer ? 'Local review recorded' : 'Confirm local draft review', icon: 'check', onClick: approve, disabled: disabled || !reviewChecked || !draft.draft_digest || Boolean(receipt) || reviewedOnServer || draft.routing?.overall_state !== 'READY_FOR_LOCAL_REVIEW', loading: busy === 'approve', waiting: waitLeft('approve') > 0 })
        : null;

  // The bar's action changed under the finger: ignore taps for PHONE_ACTION_SETTLE_MS (attack r21 phone #3).
  const phoneActionKey = phoneAction?.key || '';
  const phoneActionRef = useRef({ key: phoneActionKey, at: 0 });
  const phoneBarObserver = useRef(null);
  if (phoneActionRef.current.key !== phoneActionKey) phoneActionRef.current = { key: phoneActionKey, at: Date.now() };
  // (round2 X, C #4) On a phone the bar changes from the evidence preview action to the evidence send action in the
  // same spot. A send action stays greyed out for PHONE_SEND_HOLD_MS with a visible "ready in a moment"
  // line, so a habitual second tap on the preview never opens the send dialog; the two-step dialog still follows.
  const [, setPhoneHoldTick] = useState(0);
  const phoneSendHeld = PHONE_SEND_KEYS.includes(phoneActionKey) && Date.now() - phoneActionRef.current.at < PHONE_SEND_HOLD_MS;
  useEffect(() => {
    if (!phoneSendHeld) return undefined;
    const timer = setTimeout(() => setPhoneHoldTick((tick) => tick + 1), Math.max(0, PHONE_SEND_HOLD_MS - (Date.now() - phoneActionRef.current.at)) + 20);
    return () => clearTimeout(timer);
  }, [phoneSendHeld, phoneActionKey]);
  // One plain line under a greyed-out bar button saying what to do first (never while a request is running).
  const phoneReason = phoneSendHeld && !phoneAction.disabled ? PHONE_SEND_HOLD_TEXT
    : !phoneAction || !phoneAction.disabled || phoneAction.loading || phoneAction.waiting || !state ? null
    : phoneAction.key === 'aup' ? (description.trim() ? null : 'Type what you sell first.')
    : phoneAction.key === 'draft' ? (caseItem ? null : 'Pick a case first.')
    : phoneAction.key === 'approve' ? (draft ? approveLockReason({ sessionExpired: error?.status === 401, draft, receipt, reviewedOnServer, reviewChecked }) : null)
    : null;
  // The bar's real height (button plus reason line) keeps the page end clear of it.
  const phoneBarRef = useCallback((node) => {
    if (phoneBarObserver.current) { phoneBarObserver.current.disconnect(); phoneBarObserver.current = null; }
    if (!node || typeof ResizeObserver === 'undefined') { document.documentElement.style.removeProperty('--phone-bar-h'); return; }
    const apply = () => document.documentElement.style.setProperty('--phone-bar-h', `${Math.ceil(node.getBoundingClientRect().height)}px`);
    apply();
    phoneBarObserver.current = new ResizeObserver(apply);
    phoneBarObserver.current.observe(node);
  }, []);
  const phoneActionClick = () => {
    if (Date.now() - phoneActionRef.current.at < PHONE_ACTION_SETTLE_MS) return;
    if (phoneSendHeld) return;
    phoneAction?.onClick?.();
  };

  // Reset from step 02/03 unmounts the clicked button; focus goes to step 01's Reset demo once the reset ends
  // (attack r21 desktop #6), not to the page.
  const resetDemoButton = <Button data-testid="demo-reset" icon="refresh" tone="ghost" disabled={disabled} loading={busy === 'reset'} waiting={waitLeft('reset') > 0} onClick={() => setResetConfirm(true)}>Reset demo</Button>;
  const runReset = () => { setResetConfirm(false); openStage('compliance', { updateHash: true, scroll: true }); inject('reset'); focusWhenIdle(['#compliance [data-testid="demo-reset"]', '#stage-trigger-compliance'], { scroll: 'fallback' }); };

  return <div className={`app-shell${phoneAction ? ` has-phone-action phone-action-${phoneAction.key}` : ''}${typing ? ' is-typing' : ''}`}>
    <a className="skip-link" href="#main">Skip to console</a>
    {draftConfirm && <DraftConfirmDialog description={description} amount={invoiceAmountValue(invoiceAmount)} currency="USD"
      route={countryCheck ? `${countryCheck.seller_country} → ${countryCheck.buyer_country}` : null} expired={draftExpired}
      returnFocus={['[data-testid="invoice-create"]', '[data-testid="phone-action-invoice"]']}
      onCancel={() => { if (draftExpired) focusWhenIdle(['[data-testid="aup-review"]', '[data-testid="phone-action-aup"]', '#stage-trigger-compliance']); setDraftConfirm(false); }}
      onCreate={async () => { setDraftConfirm(false); await createInvoice(); }} />}
    {resetConfirm && <ResetConfirmDialog onCancel={() => setResetConfirm(false)} onReset={runReset} />}
    <header className="topbar" data-hosted={hosted ? 'true' : undefined} inert={warningOpen || draftConfirm || resetConfirm ? true : undefined}>
      <a className="brand" href="#main" aria-label="TradeGlot console"><span className="brand-mark"><Icon name="shield" size={23} /></span><span>TradeGlot<small>MERCHANT EVIDENCE BUFFER</small></span></a>
      <nav aria-label="Additional workspace"><a href="#analytics" onClick={() => { setAnalyticsExpanded(true); setAnalyticsOpen(true); }}>All orders</a><a href="/dashboard.html" data-testid="topbar-dashboard">Dashboard</a><a href="/scenarios.html" data-testid="topbar-scenarios">Scenarios</a><a href="/proof.html" data-testid="topbar-proof">Proof</a><a href="/evidence.html" data-testid="topbar-evidence">How it was measured</a></nav>
      <div className={hosted ? 'environment environment-hosted' : 'environment'}><span id="pwa-install-slot" className="pwa-install-slot" />{hosted ? <HostedBadge guideChooser={guideChooser} sandboxReads={sandboxReads} sandboxSend={sandboxSend} /> : <Badge tone="blue" dot>LOCAL DEMO</Badge>}{!hosted && <TopbarSandbox connected={sandbox?.status === 'connected'} disabled={disabled} loading={busy === 'connect'} onConnect={connectSandbox} />}<span className="avatar" title="TradeGlot demo user">TG</span></div>
    </header>

    <main id="main" tabIndex={-1} inert={warningOpen || draftConfirm || resetConfirm ? true : undefined} className="main-content" data-testid={state ? "session-ready" : "session-unavailable"}>
      <div className="page-top">
      <header className="hero hero-compact" aria-labelledby="page-title">
        <div><div className="eyebrow"><span className="tiny-dot" /> FOR SMALL PAYPAL SELLERS</div><h1 id="page-title">Check a sale before you ship. Prepare your evidence if PayPal asks.</h1><div className="hero-actions"><button type="button" className="hero-example-link" data-testid="hero-try-example" onClick={() => document.querySelector('[data-testid="country-try-example"]')?.click()}>Run the step 1 example</button><a className="hero-proof-link" href="/proof.html" data-testid="hero-proof-link">Proof and receipts</a><a className="hero-local-link" href="https://github.com/jiarong0423/payguard-ai/releases/download/demo-package-20261109/tradeglot-demo.zip" target="_blank" rel="noopener noreferrer" title="Same demo, one command, no keys." aria-label="Download the demo (11 MB). Same demo, one command, no keys." data-testid="hero-download-demo"><svg className="download-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.9" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M12 4v10.5" /><path d="m7.5 10.5 4.5 4.5 4.5-4.5" /><path d="M5 19.25h14" /></svg><span>Download the demo (11 MB)</span></a></div></div>
      </header>

      <section className="start-here" data-testid="start-here" aria-labelledby="start-here-title">
        <h2 id="start-here-title" className="start-here-title">Start here:</h2>
        <div className="start-here-actions">{START_HERE.map(([scenario, icon, label]) => <a key={scenario} className="start-here-link" href={`#guide-${scenario}`} data-testid={`start-here-${scenario}`} onClick={(event) => { event.preventDefault(); window.history.pushState(null, '', `#guide-${scenario}`); setActiveStage(GUIDE_STAGE[scenario]); askGuide(scenario); }}><Icon name={icon} size={16} /><Label text={label} /></a>)}</div>
      </section>
      </div>

      <nav className="journey" aria-label="Three-stage evidence buffer">
        {[
          ['01', 'shield', 'Policy pre-check', '#compliance'],
          ['02', 'chart', 'Sales spike', '#velocity'],
          ['03', 'file', 'Dispute evidence', '#disputes'],
        ].map(([number, icon, title, href], index) => <a className={`journey-step ${activeStage === href.slice(1) ? 'is-active' : stepStatus[href.slice(1)].tone === 'green' ? 'is-done' : 'is-upcoming'}`} href={href} aria-current={activeStage === href.slice(1) ? 'step' : undefined} onClick={(event) => { event.preventDefault(); openStage(href.slice(1), { updateHash: true, scroll: true }); }} key={number}><span className={`journey-icon journey-icon-${index}`}><Icon name={icon} size={22} /></span><div><strong><Label text={title} /></strong><small className={`journey-status journey-status-${stepStatus[href.slice(1)].tone}`} data-testid={`step-status-${href.slice(1)}`}>{stepStatus[href.slice(1)].label}</small></div>{index < 2 && <Icon name="arrow" className="journey-arrow" />}</a>)}
        <span className="sr-only journey-where" data-testid="where-am-i">Step {['compliance', 'velocity', 'disputes'].indexOf(activeStage) + 1} of 3 · {{ compliance: 'Policy pre-check', velocity: 'Sales spike', disputes: 'Dispute evidence' }[activeStage]}</span>
        <span className="journey-rail" aria-hidden="true" style={{ '--journey-progress': ['compliance', 'velocity', 'disputes'].indexOf(activeStage) }} />
      </nav>

      <div className="feedback-region" aria-live="polite" aria-atomic="true">
        {loading && <div className="message message-info"><span className="spinner" />Creating an isolated demo session and loading backend state.</div>}
        {error && <div className="message message-error" role="alert" data-testid="global-error"><Icon name="alert" /><div><strong>{error.status === 401 ? 'Demo session expired' : error.code === 'backend_unavailable' ? 'No connection' : error.retryAt ? 'Please wait' : 'Action not completed'}</strong><span>{waitFailureMessage(error)}<PaypalIssueNote error={error} />{bootRetryAt > now ? <span className="wait-line" data-testid="retry-wait"> Retrying automatically in {Math.ceil((bootRetryAt - now) / 1000)} second{Math.ceil((bootRetryAt - now) / 1000) === 1 ? '' : 's'}.</span> : <WaitLine until={error.retryAt} now={now} testId="retry-wait" />}</span></div>{(!state || error.status === 401) && <Button data-testid="reconnect" disabled={loading || Boolean(busy)} waiting={waitLeft('boot') > 0 || bootRetryAt > now} icon="refresh" onClick={reconnect}>Reconnect</Button>}<button className="icon-button" aria-label="Dismiss error message" onClick={() => setError(null)}><Icon name="close" /></button></div>}
        {notice && <div className="message message-success"><Icon name="check" />{notice}</div>}
        {info && <div className="message message-info" data-testid="console-info" data-kind={info.kind}><Icon name="info" />{info.text}<button type="button" className="icon-button" aria-label="Dismiss message" data-testid="console-info-dismiss" onClick={() => setInfo(null)}><Icon name="close" /></button></div>}
      </div>

      <StageAccordion id="compliance" number="01" title="Policy pre-check" subtitle="Check your item before you invoice." icon="shield" status={<RoleBadge />} actions={<div className="demo-actions">{activeStage === 'compliance' && resetDemoButton}</div>} open={activeStage === 'compliance'} onOpen={(stage) => openStage(stage, { updateHash: true })}>
        <div className="compliance-layout"><div className="invoice-editor"><div className="description-toolbar"><label className="mini-heading description-label" htmlFor="description">Product or service</label><div className="description-presets"><span>Quick tests</span><button disabled={Boolean(busy)} onClick={() => editDescription('Handcrafted ceramic coffee cup — set of two')}>Standard Item</button><button disabled={Boolean(busy)} onClick={() => editDescription('Guaranteed 30% ROI investment package')}>High-risk Claim</button></div></div><textarea data-testid="aup-description" id="description" maxLength={4000} value={description} onChange={(event) => editDescription(event.target.value)} rows={3} disabled={Boolean(busy)} aria-invalid={description.length > DESCRIPTION_LIMIT || undefined} aria-describedby={description.length > DESCRIPTION_LIMIT ? 'description-note' : undefined} /><div className="editor-bottom"><span className={`text-dim ${description.length > 200 ? 'over-limit' : ''}`} data-testid="aup-char-count">{description.length} / 200</span><Button data-testid="aup-review" icon="shield" tone="blue" onClick={runPolicyCheck} disabled={disabled || !description.trim()} blocked={Boolean(descriptionProblem(description))} aria-describedby={descriptionProblem(description) ? 'description-note' : undefined} waiting={waitLeft('aup') > 0} loading={busy === 'aup'}>Run Policy Check</Button></div>{descriptionProblem(description) && <p id="description-note" className="field-note" role="status" data-testid="aup-description-note">{descriptionProblem(description)}</p>}</div><div data-testid="aup-result" data-state={aupPhase} aria-live="polite" className={`aup-result ${aup?.findings?.length ? 'aup-warning' : ''}`}><div className="result-heading"><span className="result-symbol"><Icon name={aup?.findings?.length ? 'alert' : 'shield'} size={25} /></span><div><span className="meta-label" data-testid="aup-result-label">{/* (optimise r24) No "REVIEW SIGNAL" before a check has run. */}{aup ? (aup.match_status === 'REVIEW_SIGNAL' ? 'REVIEW SIGNAL' : 'POLICY CHECK') : aupPhase === 'loading' ? 'CHECKING' : countryCheck ? 'COUNTRY CHECK DONE' : 'NOT CHECKED YET'}</span><h3>{aupPhase === 'loading' ? 'Checking description' : aupPhase === 'error' ? 'Check incomplete; try again' : !aup ? (countryCheck ? 'Country result is in the country card' : 'Waiting for description check') : aup.match_status === 'REVIEW_SIGNAL' ? 'Review signal matched' : 'No demo rule matched'}</h3></div></div>{aup ? <><div className="finding-list">{aup.findings.length ? aup.findings.map((finding) => <Badge tone="amber" key={finding.category}>{findingLabels[finding.category] || 'Needs review'}</Badge>) : <Badge tone="muted">No configured demo keyword matched</Badge>}</div><p>{aup.recommendation}</p><AupValidFor key={`valid-${aup.evaluation_id}`} expiresAt={aup.expires_at} /><AupExpiryWarning key={aup.evaluation_id} expiresAt={aup.expires_at} onKeep={keepAupResult} blocked={Boolean(busy) || waitLeft('aup') > 0} loading={busy === 'aup'} productConfirmed={Boolean(productConfirm)} />{categorySignal?.status !== 'OFF' && <p data-testid="aup-category-signal" data-state={categorySignal?.status || 'NONE'} className="text-dim">{categorySignalLabel(categorySignal)}</p>}{/* (r32 J1) "Product lookup is off" is a console setting, not a seller result: it sits in Limits and safety. */}{productRef?.status !== 'OFF' && <ProductReference result={productRef} confirmation={productConfirm} busy={Boolean(busy)} onConfirm={confirmProduct} />}</> : <><p data-testid="aup-pane-caption">The description check shows here. The country rules result appears in the country card.</p>{productConfirm && <p className="text-dim" data-testid="product-confirmation-kept">{productConfirm.choice === 'CONFIRMED' ? `Your product confirmation is kept for the review ZIP: ${productConfirm.card.title}.` : 'Your answer that none of the catalogue products is yours is kept for the review ZIP.'}</p>}</>}</div></div>
        {clearedOnReload && !countryCheck && !aup && !lastCountryCheck && <p className="sandbox-reminder country-lost" data-testid="result-cleared-note" role="status">Result cleared on reload. Press Run again.</p>}
        {countryLost && <p className="sandbox-reminder country-lost" data-testid="country-check-lost" role="status">Run the country check again: the {lastCountryCheck.seller_country} → {lastCountryCheck.buyer_country} result ended with the expired session.</p>}
        <div className="stage-block"><CountryRules key={`country-${sessionRef.current?.session_id || 'no-session'}-${countryResetCount}`} session={sessionRef.current} onResult={onCountryResult} onContinue={continueToDraft} onSessionExpired={panelSessionExpired} onBusy={setCountryBusy} onExample={() => editDescription(EXAMPLE_DESCRIPTION)} /></div>
        <details id="sandbox-draft" className="sandbox-details stage-block-details" open={sandboxOpen} onToggle={(event) => setSandboxOpen(event.currentTarget.open)}><summary><Icon name="link" size={16} /><span>PayPal Sandbox draft (optional)</span><span data-testid="sandbox-status"><Badge tone={sandbox?.status === 'connected' ? 'green' : 'muted'} dot>{hosted && !sandboxReads ? 'Local run only' : sandbox?.status === 'not_configured' ? 'Awaiting connection' : operatorLabel(sandbox?.status, 'Status not loaded')}</Badge></span></summary><div className="sandbox-inner">{(!hosted || sandboxReads) && <p className="text-dim" data-testid="sandbox-optional-note">{hosted ? (sandboxSend ? 'Optional: connect to read the author\'s Sandbox test disputes and make one capped evidence send.' : 'Optional: connect to read Sandbox test disputes (read-only).') : 'Optional: connect your own Sandbox to create an unsent draft.'}</p>}<div className="sandbox-connect">{hosted && !sandboxReads ? <p className="hosted-note" data-testid="hosted-note-sandbox">{HOSTED_NOTES.sandbox}</p> : <Button data-testid="sandbox-connect" icon="link" disabled={disabled} hidden={sandbox?.status === 'connected'} loading={busy === 'connect'} waiting={waitLeft('connect') > 0} onClick={connectSandbox}>Connect US Sandbox</Button>}</div>{sandbox?.evidence_receipt && <p className="sandbox-readback">Connection evidence: {sandboxEvidenceLabel(sandbox.evidence_receipt)} · {sandboxReadbackLabel(sandbox.evidence_receipt.separate_get_readback)}</p>}<div className="invoice-draft-form"><label>Draft amount <span className="text-dim">USD</span><input id="invoice-amount" type="text" inputMode="decimal" value={invoiceAmount} maxLength={20} disabled={Boolean(busy)} aria-invalid={amountNote ? true : undefined} aria-describedby={amountNote ? 'invoice-amount-note' : undefined} onChange={(event) => editInvoiceAmount(event.target.value)} /></label>{amountNote && <p id="invoice-amount-note" className="field-note" role="alert" data-testid="invoice-amount-note">{amountNote}</p>}<label className="checkbox-label"><input data-testid="invoice-confirm" type="checkbox" checked={invoiceChecked} disabled={Boolean(busy)} onChange={(event) => setInvoiceChecked(event.target.checked)} /><span>I reviewed the description and amount and confirm that this action creates a Sandbox draft only.</span></label><Button data-testid="invoice-review" icon="check" aria-describedby="invoice-lock-reason" disabled={disabled || countryHeld || !invoiceChecked || !aup || aupConsumed || description.length > 200} loading={busy === 'invoice-review'} waiting={waitLeft('invoice-review') > 0} onClick={reviewInvoice}>Confirm Draft Context</Button>{hosted ? <p className="hosted-note" data-testid="hosted-note-invoice">{HOSTED_NOTES.invoice}</p> : <Button data-testid="invoice-create" icon="file" tone="blue" aria-describedby="invoice-lock-reason" disabled={disabled || countryHeld || !invoiceReview || !invoiceChecked || sandbox?.status !== 'connected'} loading={busy === 'invoice'} waiting={waitLeft('invoice') > 0} onClick={() => setDraftConfirm(true)}>Create Sandbox draft</Button>}<LockReason testId="invoice-lock-reason" reason={draftLockReason({ sessionExpired: error?.status === 401, hosted, countryHeld, aup, aupExpired, aupConsumed,
          descriptionTooLong: description.length > DESCRIPTION_LIMIT, invoiceChecked, invoiceReview, invoice, connected: sandbox?.status === 'connected' })} /></div>{!countryHeld && !countryCheck && <p className="sandbox-reminder" data-testid="invoice-country-reminder">Shipping abroad? Check the country rules above first. This does not block the draft.</p>}{countryHeld && <p className="text-dim" data-testid="invoice-country-blocked">{countryStale ? 'No draft: the last country check stopped this sale. Check again after your change.' : 'No draft: a country rule stops this shipment (see the result above).'}</p>}{invoiceReview && <p className="sandbox-readback">{operatorLabel('PAYLOAD_DIGEST_BOUND')} · <ValidFor expiresAt={invoiceReview.expires_at} testId="invoice-valid-for" /></p>}{invoice && <p className="sandbox-reminder" data-testid="invoice-shipping-reminder">Reminder: this draft has no shipping country. Add the buyer's country in PayPal before you send the invoice.{countryCheck ? ` The checked route (${countryCheck.seller_country} to ${countryCheck.buyer_country}) is in the draft's private memo.` : ''}</p>}{invoice && <p className="sandbox-readback" data-testid="invoice-readback">Sandbox invoice draft created · <span data-testid="invoice-id">{maskInvoiceId(invoice.invoice_id)}</span> · {operatorLabel(invoice.status)} · {sandboxEvidenceLabel(invoice.evidence_receipt)} · {sandboxReadbackLabel(invoice.evidence_receipt.separate_get_readback)} · {operatorLabel(invoice.external_send)}</p>}</div></details>
        <GuideLive key={`preflight-${sessionRef.current?.session_id || 'no-session'}`} scenario="preflight" session={sessionRef.current} Disclosure={StepSection} Badge={Badge} onChooser={setGuideChooser} request={guideRequest} onSessionExpired={panelSessionExpired} />
        <StepMore id="compliance"><StepSection id="sources-source_compliance" title="Sources, policy check, and AI brief" subtitle="Official sources, demo claim check, AI summary, technical details" icon="link" open={Boolean(sourcesOpen.source_compliance)} onToggle={(next) => setSourcesOpen((current) => ({ ...current, source_compliance: next }))} testId="sources-toggle-source_compliance">
          <SecondaryStageTabs stage="source_compliance" activeTab={openSecondary.source_compliance} onSelectTab={toggleSecondary} referenceProps={referenceProps} aiAvailable={aup?.match_status === 'REVIEW_SIGNAL' && !aupConsumed && !disabled && !busy && !aiBusyStage} brief={aiBriefs.source_compliance} notice={aiNotices.source_compliance} aiLoading={aiBusyStage === 'source_compliance'} onGenerateAi={generateAiBrief} hosted={hosted} techContent={<div className="sandbox-tech-details">{aup && <p className="result-footnote"><span data-testid="aup-baseline-id">Baseline id (internal name kept for compatibility): {aup.policy_version}</span> · {operatorLabel(aup.compliance_decision)} · <strong data-testid="aup-applicability">{operatorLabel(aup.current_policy_applicability)}</strong> · valid until {utcLabel(aup.expires_at)}</p>}<dl className="provider-context" data-testid="provider-context">{[
            ['Demo market', 'United States'],
            ['Provider environment', 'PayPal Sandbox'],
            ['Developer login', 'Existing PayPal login; live account type not inferred'],
            ['Merchant role', 'Fictitious Business sandbox seller in the demo scenario'],
            ['Buyer role', 'Fictitious Personal sandbox account when required'],
            ['Sandbox seller country', 'Unconfirmed until Dashboard readback'],
            ['Invoicing eligibility', invoice?.evidence_receipt?.evidence_class === 'AUTHENTIC_SANDBOX_RESPONSE' ? 'Sandbox draft creation observed; broader eligibility unconfirmed' : 'Unconfirmed until bounded provider evidence'],
            ['External action', 'Disabled by default; explicit Sandbox OAuth and unsent draft only'],
          ].map(([label, value]) => <div key={label}><dt>{label}</dt><dd>{value}</dd></div>)}</dl></div>} />
        </StepSection><LimitsDrawer id="compliance">{productRef?.status === 'OFF' && <p className="text-dim" data-testid="product-lookup-off">Product lookup is off on this console (no Channel3 key), so no product cards are shown. The policy result does not use it.</p>}<p className="aup-policy-link"><a data-testid="aup-policy-link" href={AUP_POLICY_URL} target="_blank" rel="noopener noreferrer">PayPal US Acceptable Use Policy (official source)</a><span>US policy only. A match is a prompt to review, not a decision.</span></p><p className="result-footnote">A merchant must review the actual offering and policy.</p><p data-testid="aup-invoice-limit" className="text-dim">Invoice drafts allow 200 description characters. {description.length > 200 && 'Shorten the description and run the check again before continuing.'}</p><p className="text-dim">Connects only when you press Connect. Creates an unsent Sandbox draft only. Each receipt says whether it is a live Sandbox result or a demo test.</p></LimitsDrawer></StepMore>
        <div className="stage-next"><span>Next: the orders behind a sales spike.</span><Button icon="arrow" tone="secondary" onClick={() => openStage('velocity', { updateHash: true, scroll: true, focus: true })}>Next: sales burst</Button></div>
      </StageAccordion>

      <StageAccordion id="velocity" number="02" title="Sales spike" subtitle="Find the orders that need proof of delivery." icon="chart" status={<Badge tone={velocity?.alert ? 'amber' : velocity?.transaction_count > 0 && velocity?.status === 'normal' ? 'green' : 'muted'} dot>{velocity ? velocity.status === 'review_velocity' ? 'Needs review' : velocity.transaction_count > 0 ? 'Within demo threshold' : 'No in-window data' : 'Waiting'}</Badge>} actions={<div className="demo-actions"><Button data-testid="demo-burst" icon="bolt" tone={velocity?.transaction_count ? 'secondary' : 'blue'} disabled={disabled} loading={busy === 'burst'} waiting={waitLeft('burst') > 0} onClick={() => inject('burst')}>Load sales burst</Button>{activeStage === 'velocity' && resetDemoButton}</div>} open={activeStage === 'velocity'} onOpen={(stage) => openStage(stage, { updateHash: true })}>
        <div className="stage-body"><div className="stage-main">
        <div className="metrics-grid velocity-metrics">
          <Metric label="Window sales" value={velocity?.transaction_count ? velocity.total_amount : '—'} unit={velocity?.transaction_count ? velocity.currency || 'USD' : ''} icon="chart" detail={`Last ${velocity?.window_hours ?? '—'}h · demo`} />
          <Metric testId="velocity-ratio" label="Sales vs. usual" value={velocity?.transaction_count ? velocity.ratio : '—'} unit={velocity?.transaction_count ? '× the usual hourly sales' : ''} icon="bolt" detail={<>{`Review threshold ${velocity?.threshold ?? '—'}×`}<span className="metric-baseline-note" data-testid="velocity-baseline-note">The baseline here is a local demo setting, not a PayPal limit.</span></>} alert={velocity?.alert === true} />
          <Metric label="Orders in last hour" value={velocity?.transaction_count ?? '—'} unit="orders" icon="layers" detail="Unique orders" />
        </div>
        <div className={`velocity-summary ${velocity?.alert ? 'velocity-alert' : ''}`}><div><Icon name={velocity?.alert ? 'alert' : 'chart'} /><span>{velocity?.alert ? `Sales are ${velocity.ratio}× usual. Check the orders.` : velocity?.transaction_count > 0 ? 'Orders are within the usual range.' : 'No sales loaded yet. Press Load sales burst.'}</span></div>{velocity?.alert && <small className="text-dim" data-testid="velocity-inspect-note">Opens the table of orders in this window, so you can check each one.</small>}{velocity?.alert && <Button data-testid="velocity-inspect-transactions" className="velocity-inspect" icon="arrow" onClick={() => { setVelocityFold(true); setVelocityView('orders'); window.requestAnimationFrame(() => document.getElementById('velocity-quick-filter')?.focus()); }} disabled={disabled}>Inspect orders</Button>}<span className="velocity-window"><Icon name="clock" size={14} />{dateLabel(velocity?.window_end)}</span></div>
        <details className="sandbox-details stage-fold" data-testid="velocity-fold" open={velocityFold} onToggle={(event) => setVelocityFold(event.currentTarget.open)}><summary>Hourly chart, orders table and the records behind the alert</summary><div className="segmented-row"><div className="segmented" role="tablist" aria-label="Sales view" onKeyDown={(event) => tabKeyDown(event, ['chart', 'orders'], velocityView, setVelocityView, (key) => `velocity-view-${key}`)}>{[['chart', 'Chart'], ['orders', 'Orders table']].map(([key, label]) => <button key={key} type="button" role="tab" id={`velocity-view-${key}`} data-testid={`velocity-view-${key}`} aria-selected={velocityView === key} tabIndex={velocityView === key ? 0 : -1} aria-controls={`velocity-pane-${key}`} className={velocityView === key ? 'is-active' : ''} onClick={() => setVelocityView(key)}>{label}</button>)}</div></div>
        <div id="velocity-pane-chart" className="velocity-pane" role="tabpanel" aria-labelledby="velocity-view-chart" hidden={velocityView !== 'chart'}>{velocity && <Suspense fallback={<div className="analytics-loading" role="status"><span className="spinner" />Loading the hourly chart.</div>}><VelocityChart velocity={chartVelocity} transactions={state?.transactions} compact={narrowScreen} /></Suspense>}{velocity && narrowScreen && <PhoneChartLegend />}<SpikeRecordsCard velocity={velocity} transactions={state?.transactions} /></div>
        <div id="velocity-pane-orders" className="velocity-pane" role="tabpanel" aria-labelledby="velocity-view-orders" hidden={velocityView !== 'orders'}>
        <div className="grid-caption"><span><span className="tiny-dot" /> DEMO ORDERS</span></div>
        <div className="velocity-grid-tools"><label htmlFor="velocity-quick-filter">Filter orders</label><input data-testid="velocity-filter" id="velocity-quick-filter" type="text" maxLength={200} value={velocityQuickFilter} onChange={(event) => setVelocityQuickFilter(event.target.value)} placeholder="Order, amount or time" disabled={disabled} /></div>
        <div className="transaction-grid" data-testid="velocity-grid" aria-label="Demo order table"><Suspense fallback={<span className="grid-loading" role="status">Loading the table</span>}><AgGridReact theme={gridTheme} rowData={state?.transactions || []} columnDefs={columns} defaultColDef={{ sortable: true, resizable: true, filter: true }} getRowId={({ data }) => data.order_id} getRowClass={({ data }) => data?.order_id === selectedVelocityTransaction?.order_id ? 'ag-row-selected-transaction' : ''} quickFilterText={velocityQuickFilter} onGridReady={({ api }) => { velocityGridApi.current = api; }} onRowClicked={({ data }) => setSelectedVelocityTransaction(data)} rowHeight={46} headerHeight={46} animateRows loading={loading || !state} overlayLoadingTemplate="Loading transactions" overlayNoRowsTemplate="Select Load sales burst above to see transactions" /></Suspense></div>
        {selectedVelocityTransaction && <section className="velocity-selected-detail" data-testid="velocity-selected-detail" aria-label="Selected transaction details"><div className="velocity-selected-heading"><div><span className="meta-label">SELECTED ORDER</span><h3>{selectedVelocityTransaction.order_id}</h3></div><Badge tone={velocity?.status === 'review_velocity' ? 'amber' : velocity?.status === 'normal' ? 'green' : 'muted'}><span data-testid="velocity-stage-status">{velocityStageStatusLabel(velocity)}</span></Badge></div><dl><div><dt>Order reference</dt><dd>{selectedVelocityTransaction.order_id}</dd></div><div><dt>Amount</dt><dd>{selectedVelocityTransaction.amount ?? '—'} {selectedVelocityTransaction.currency || '—'}</dd></div><div><dt>Captured at</dt><dd>{dateLabel(selectedVelocityTransaction.occurred_at)}</dd></div><div><dt>Stage evidence checklist</dt><dd>Check capacity and tracking or delivery records; this demo has none.</dd></div></dl><p>This signal does not prove fraud, check delivery or predict what PayPal will do.</p></section>}
        </div>
        </details>
        </div><aside className="stage-side">
        <GuideLive key={`velocity-${sessionRef.current?.session_id || 'no-session'}`} scenario="velocity" session={sessionRef.current} Disclosure={StepSection} Badge={Badge} onChooser={setGuideChooser} request={guideRequest} onSessionExpired={panelSessionExpired} />
        <StepMore id="velocity"><StepSection id="sources-velocity_guard" title="Sources, policy check, and AI brief" subtitle="Official sources, demo claim check, AI summary, technical details" icon="link" open={Boolean(sourcesOpen.velocity_guard)} onToggle={(next) => setSourcesOpen((current) => ({ ...current, velocity_guard: next }))} testId="sources-toggle-velocity_guard">
          <SecondaryStageTabs stage="velocity_guard" activeTab={openSecondary.velocity_guard} onSelectTab={toggleSecondary} referenceProps={referenceProps} aiAvailable={velocity?.status === 'review_velocity' && !disabled && !busy && !aiBusyStage} brief={aiBriefs.velocity_guard} notice={aiNotices.velocity_guard} aiLoading={aiBusyStage === 'velocity_guard'} onGenerateAi={generateAiBrief} hosted={hosted} techContent={<div className="velocity-details"><span data-testid="velocity-baseline">Baseline {velocity?.baseline_amount_per_hour ?? '—'} USD/hour · {operatorLabel(velocity?.baseline_provenance)} · {utcLabel(velocity?.baseline_window_start)} to {utcLabel(velocity?.baseline_window_end)}</span><span>{state?.policy_version || 'POLICY —'}</span></div>} />
        </StepSection><LimitsDrawer id="velocity"><p><Icon name="lock" size={13} /> It does not predict PayPal account limits or start any payment.</p></LimitsDrawer></StepMore>
        <div className="stage-next"><span>Next: answer a dispute.</span><Button icon="arrow" tone="secondary" onClick={() => openStage('disputes', { updateHash: true, scroll: true, focus: true })}>Next: dispute evidence</Button></div>
        </aside></div>
      </StageAccordion>

      <StageAccordion id="disputes" number="03" title="Dispute evidence" subtitle="Prepare, download, then you confirm." icon="file" status={<RoleBadge />} actions={<div className="demo-actions"><Button data-testid="demo-dispute" icon="file" tone="blue" hidden={Boolean(state?.disputes?.length)} disabled={disabled} loading={busy === 'dispute'} waiting={waitLeft('dispute') > 0} onClick={() => inject('dispute')}>Load dispute case</Button>{activeStage === 'disputes' && resetDemoButton}</div>} open={activeStage === 'disputes'} onOpen={(stage) => openStage(stage, { updateHash: true })}>
        <div className="stage-body"><div className="stage-main">
        <div className="inner-tabs" role="tablist" aria-label="Step 03 views" data-board-open={boardOpen ? 'true' : 'false'}><button type="button" role="tab" id="disputes-tab-review" aria-selected={!boardOpen} className={`inner-tab ${!boardOpen ? 'is-active' : ''}`} data-testid="disputes-tab-review" onClick={() => setBoardExpanded(false)}>Case review</button><button type="button" role="tab" id="disputes-tab-board" aria-selected={boardOpen} className={`inner-tab ${boardOpen ? 'is-active' : ''}`} data-testid="disputes-tab-board" onClick={() => setBoardExpanded(true)}>Deadline board</button></div>
        <div className="dispute-layout"><div className="case-list"><div className="mini-heading"><span>Case queue</span><span className="text-dim">Demo cases</span></div>{state?.disputes?.length ? state.disputes.map((item) => <button key={item.case_ref} className={`case-card ${caseItem?.case_ref === item.case_ref ? 'case-selected' : ''}`} disabled={Boolean(busy)} onClick={() => { if (caseItem?.case_ref === item.case_ref) return; invalidateAi(); setSelectedCase(item.case_ref); setDraft(null); setReceipt(null); setReviewChecked(false); }}><div><Icon name="file" /><strong>{item.case_ref}</strong><Badge tone="amber">{operatorLabel(item.reason)}</Badge></div><span>{item.order_ref}</span><small>{dateLabel(item.opened_at)} · {operatorLabel(item.status)}</small><small className="case-due" data-testid={`case-due-${item.case_ref}`}>{dueLabel(item.seller_response_due_date)}</small></button>) : <div className="empty-state"><Icon name="file" size={32} /><strong>No dispute cases</strong><p>Use “Load dispute case” above to start.</p></div>}<details className="case-more" data-testid="case-more"><summary>More views: deadlines and proof records</summary><a className="case-note dashboard-cta" href="/dashboard.html" data-testid="dispute-dashboard-cta"><Icon name="layers" size={15} /><p>See all deadlines</p></a><a className="case-note dashboard-cta proof-cta" href="/proof.html" data-testid="dispute-proof-cta"><Icon name="check" size={15} /><p>See the proof records</p></a></details></div><div className="evidence-workspace"><div className="evidence-toolbar"><div><span className="meta-label">CASE REVIEW</span><h3>{receipt || reviewedOnServer ? 'Local draft review recorded' : draft ? 'Draft created · awaiting human review' : caseItem ? 'Prepare objective evidence draft' : 'You approve every step'}</h3></div><Button data-testid="dispute-draft" icon="file" tone={draft ? 'secondary' : 'blue'} disabled={disabled || !caseItem || caseItem.status === 'local_draft_reviewed'} loading={busy === 'draft'} waiting={waitLeft('draft') > 0} onClick={getDraft}>{busy === 'draft' ? 'Preparing…' : 'Prepare evidence draft'}</Button></div>{draft ? <><div className="dispute-route" data-testid="dispute-route"><div><span>Response readiness</span>{/* (r34 #9) After the local review the server's routing still reads "Ready for human review"; the summary says what is next, and the server values stay in Technical details. */}<strong data-testid="dispute-readiness">{receipt || reviewedOnServer ? 'Reviewed · next: preview and send' : operatorLabel(draft.routing?.overall_state)}</strong><small>{operatorLabel(draft.routing?.reason)} · {operatorLabel(draft.routing?.dispute_life_cycle_stage)} · {operatorLabel(draft.routing?.status)}</small><small data-testid="dispute-due-at">Due {dateLabel(draft.routing?.seller_response_due_date)}{dueLabel(draft.routing?.seller_response_due_date) ? ` · ${dueLabel(draft.routing?.seller_response_due_date)}` : ''}</small>{!(receipt || reviewedOnServer) && <small data-testid="dispute-actions">Draft ready: review it below. PayPal action for this case: {operatorLabels(draft.routing?.available_actions).join(', ') || 'None'}</small>}</div><Badge tone={draft.routing?.due_state === 'OPEN' ? 'green' : 'danger'}><span data-testid="dispute-due-state">{operatorLabel(draft.routing?.due_state)}</span></Badge></div><div className="requirement-list" data-testid="dispute-requirements">{draft.routing?.requirements?.map((row) => <div key={row.request_id}><div><strong>{operatorLabel(row.provider_evidence_type)}</strong><span>{operatorLabel(row.source)}</span><small>Evidence action: {operatorLabel(row.action, 'No action requested')}</small></div><Badge tone={row.requirement_state === 'STRUCTURALLY_PRESENT' ? 'green' : row.requirement_state.includes('MISSING') ? 'amber' : 'muted'}>{operatorLabel(row.requirement_state)}</Badge><small>{row.proof_count} proof record(s) · {row.accepted_attachment_count} accepted attachment(s)</small></div>)}</div>{/* (r33 M4) */}{guideOpenItems > 0 && <p className="guide-open-items text-dim" data-testid="guide-open-items">Guide items still open: {guideOpenItems}; they are not part of this draft.</p>}{draft.time_evidence && <Suspense fallback={<p className="text-dim" role="status">Loading the time evidence</p>}><TimeEvidenceView evidence={draft.time_evidence} /></Suspense>}<StepOneEvidence productConfirm={productConfirm} countryCheck={lastCountryCheck?.session === state?.session_id ? lastCountryCheck : null} lostCheck={countryLost ? lastCountryCheck : null} /><div className="privacy-strip" data-testid="internal-review-profile"><Icon name="lock" /><div><strong>Review copy ready for download</strong><span>{draft.document_redaction?.replacement_count ?? 0} personal details replaced with placeholders · check before sharing</span><small>Automatic detection is limited. Check the file yourself before sharing.</small></div><Button data-testid="download-pseudonymized-evidence" className="privacy-download" icon="file" onClick={downloadRedactedFile} disabled={disabled || !draft.document_redaction}>Download review file</Button><Button data-testid="download-internal-review-zip" icon="file" onClick={downloadReviewZip} disabled={disabled || !draft}>Download review ZIP</Button></div><div className="human-review"><label className="checkbox-label"><input type="checkbox" checked={reviewChecked || reviewedOnServer} disabled={Boolean(busy) || Boolean(receipt) || reviewedOnServer || draft.routing?.overall_state !== 'READY_FOR_LOCAL_REVIEW'} onChange={(event) => setReviewChecked(event.target.checked)} /><span>I checked the evidence and timeline. Record my review (demo only).</span></label><Button data-testid="dispute-approve" tone={receipt || reviewedOnServer ? 'secondary' : 'blue'} icon="check" aria-describedby="approve-lock-reason" onClick={approve} disabled={disabled || !reviewChecked || !draft.draft_digest || Boolean(receipt) || reviewedOnServer || draft.routing?.overall_state !== 'READY_FOR_LOCAL_REVIEW'} loading={busy === 'approve'} waiting={waitLeft('approve') > 0}>{receipt || reviewedOnServer ? 'Local review recorded' : 'Confirm local draft review'}</Button><LockReason testId="approve-lock-reason" reason={approveLockReason({ sessionExpired: error?.status === 401, draft, receipt, reviewedOnServer, reviewChecked })} /><ApprovalPayloadCard preview={evidencePreview} caseRef={draft.case_ref} hosted={hosted && !sandboxSend} /></div>{receipt && <div className="receipt" data-testid="dispute-result" tabIndex={-1}><Icon name="check" /><span>Local draft reviewed · {/* (r32 J1 J4) Plain words here; the full disclosure ("identity is not checked") is in Limits and safety. */}{receipt.reviewer === 'DEMO_OPERATOR_UNAUTHENTICATED' ? 'Demo operator (no sign-in)' : operatorLabel(receipt.reviewer)} · {dateLabel(receipt.reviewed_at)} · {operatorLabel(receipt.retention)} · <span data-testid="dispute-result-submission">{reviewSubmissionLabel(receipt, sentToShown)}</span></span></div>}{reviewedOnServer && <div className="receipt" data-testid="dispute-result-restored"><Icon name="check" /><span>{restoredReviewText(sentToShown)}</span></div>}<details className="dispute-details"><summary><Icon name="layers" size={16} /> Evidence fields and ZIP contents</summary><div className="dispute-detail-content"><div className="evidence-grid">{[['Case reason', operatorLabel(draft.evidence?.reason)], ['Carrier status', operatorLabel(draft.evidence?.carrier_status)], ['Order created', dateLabel(draft.evidence?.order_created_at)], ['Delivery event', dateLabel(draft.evidence?.delivered_at)], ['Dispute opened', dateLabel(draft.evidence?.opened_at)], ['Evidence source', operatorLabel(draft.evidence?.evidence_source)]].map(([label, value]) => <div key={label}><span>{label}</span><strong>{value || '—'}</strong></div>)}</div><div className="restricted-summary" data-testid="restricted-original-summary"><Icon name="lock" /><div><strong>Original details stay in this session</strong><span>{draft.restricted_original_summary?.proof_record_count} proof record(s) · {draft.restricted_original_summary?.attachment_count} attachment(s)</span><small>Original files are not included. Nothing is sent.</small></div></div><div className="zip-contents" data-testid="internal-review-zip-contents"><strong>Internal Review ZIP contents</strong><ul>{INTERNAL_REVIEW_ZIP_CONTENTS.map((name) => <li key={name}>{name}{name === 'product-reference.json' && <span className="step-one-tag" data-testid="zip-from-step-01">From step 01</span>}</li>)}</ul><small>Seven fixed files · generated locally · not sent to PayPal</small><small>One download for your own review: the draft, a timeline and the checks.</small></div><ScenarioMatchPanel match={draft.scenario_match} />{draft.review_reasons?.length > 0 && <p className="review-warning">Review flags: {operatorLabels(draft.review_reasons).join(', ')}</p>}</div></details></> : caseItem ? <><div className="case-summary" data-testid="case-summary"><dl>{[['Reason', operatorLabel(caseItem.reason)], ['Amount', caseItem.dispute_amount ? `${caseItem.dispute_amount.value} ${caseItem.dispute_amount.currency_code}` : '—'], ['Deadline', dueLabel(caseItem.seller_response_due_date) || 'Shown after the draft'], ['Status', operatorLabel(caseItem.status)], ['Seller Protection', 'PayPal decides if it applies']].map(([label, value]) => <div key={label}><dt>{label}</dt><dd>{value}</dd></div>)}</dl><p>Make a draft, check it, then confirm. PayPal decides the outcome.</p></div><details className="evidence-next" data-testid="evidence-next" open><summary>What you get after you prepare the draft</summary><ul><li>Required fields and a timeline, with what is still missing</li><li>The Internal Review ZIP: seven files, generated locally</li><li>A human review before anything can be sent</li></ul></details></> : <div className="evidence-placeholder"><svg className="placeholder-illustration" width="180" height="56" viewBox="0 0 180 56" fill="none" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><rect x="8" y="8" width="40" height="40" rx="8" stroke="var(--pg-color-accent)" strokeWidth="1.75" /><path d="M22 22h12M22 28h12M22 34h8" stroke="var(--pg-color-accent)" strokeWidth="1.75" /><path d="M52 28h14" stroke="var(--pg-color-subtle)" strokeWidth="1.75" strokeDasharray="3 3" /><rect x="70" y="8" width="40" height="40" rx="8" stroke="var(--pg-color-subtle)" strokeWidth="1.75" /><rect x="83" y="27" width="14" height="10" rx="2" stroke="var(--pg-color-accent)" strokeWidth="1.75" /><path d="M86 27v-3a4 4 0 0 1 8 0v3" stroke="var(--pg-color-accent)" strokeWidth="1.75" /><path d="M114 28h14" stroke="var(--pg-color-subtle)" strokeWidth="1.75" strokeDasharray="3 3" /><rect x="132" y="8" width="40" height="40" rx="8" stroke="var(--pg-color-accent)" strokeWidth="1.75" /><path d="m145 28.5 4.5 4.5 9.5-10" stroke="var(--pg-color-accent)" strokeWidth="1.75" /></svg><h3>Prepare → Download → Human review</h3><p>Make a draft, check it, then confirm. PayPal decides the outcome.</p></div>}</div></div>
        {hosted && <details key={sendNoneLeft ? 'replay-open' : 'replay'} open={sendNoneLeft || undefined} className="sandbox-details stage-fold" data-testid="replay-fold"><summary>{sandboxSend ? 'Earlier recorded send (replay, sends nothing now)' : 'Try the send: a recorded replay (nothing is sent)'}</summary><Suspense fallback={<span className="grid-loading" role="status">Loading the replay</span>}><RecordedSendReplay /></Suspense></details>}
        <details className="sandbox-details provider-disputes" data-testid="provider-disputes"><summary><Icon name="link" size={16} /><span>{providerDisputes?.source === 'paypal_sandbox' ? 'PayPal Sandbox disputes' : sandboxReads ? 'PayPal Sandbox disputes · not connected' : 'Sample PayPal cases (not real)'}</span><span data-testid="dispute-data-source"><Badge tone={providerDisputes?.source === 'paypal_sandbox' ? 'green' : 'muted'} dot>{providerDisputes?.source === 'paypal_sandbox' ? 'Sandbox' : providerDisputes?.data_source_label ? 'Sample' : providerDisputes?.error ? 'Readback unavailable' : 'Loading'}</Badge></span></summary>
          <div className="provider-disputes-body">
            <p>{providerDisputes?.source === 'paypal_sandbox' ? 'Live Sandbox disputes. Names, messages and links are not shown.' : hosted && !sandboxReads ? <span data-testid="hosted-note-disputes">{HOSTED_NOTES.disputes}</span> : 'Sample cases. Connect the Sandbox in Step 01 to see real Sandbox cases.'}</p>
            {providerDisputes?.error && <p className="text-dim">{providerDisputes.error}</p>}
            {providerDisputes?.source === 'paypal_sandbox' && providerDisputes.paypal_debug_id && <p className="text-dim" data-testid="dispute-list-debug-id">List read PayPal-Debug-Id: {providerDisputes.paypal_debug_id}</p>}
            {sendNoneLeft && <p className="hosted-note" role="status" data-testid="hosted-send-none-left">{sendCapped ? HOSTED_NOTES.capped : HOSTED_NOTES.noneLeft}</p>}
            {sandboxReads && sandbox?.status !== 'connected' && <Button data-testid="sandbox-connect-disputes" icon="link" disabled={disabled} loading={busy === 'connect'} waiting={waitLeft('connect') > 0} onClick={connectSandbox}>Connect US Sandbox</Button>}
            {/* (fix r1 U6) One cue above the list, then the two send buttons and the pairing card right under it; the
                field-by-field PayPal read of the picked dispute sits in Technical details at the end. */}
            {providerDisputes?.source === 'paypal_sandbox' && (!hosted || sandboxSend) && !evidenceSent && <p className="provider-dispute-hint" data-testid="provider-dispute-hint">Pick a dispute that is waiting for the seller.</p>}
            <div className="provider-dispute-list">{(providerDisputes?.items || []).map((row) => <button key={row.dispute_id} type="button" data-testid="provider-dispute-row" className={`case-card ${providerDisputeDetail?.dispute_id === row.dispute_id ? 'case-selected' : ''}`} disabled={disabled} onClick={() => loadProviderDispute(row.dispute_id)}><div><Icon name="file" /><strong>{displayDisputeId(row.dispute_id)}</strong><Badge tone="amber">{operatorLabel(row.reason)}</Badge></div><span>{row.dispute_amount.value} {row.dispute_amount.currency_code} · {operatorLabel(row.status)}</span><small>{operatorLabel(row.dispute_life_cycle_stage)} · {row.seller_response_due_date ? `due ${dateLabel(row.seller_response_due_date)}` : 'no due date on this case'}</small></button>)}</div>
            <div className="provider-dispute-actions">{hosted && !sandboxSend ? <p className="hosted-note" data-testid="hosted-note-evidence">{HOSTED_NOTES.evidence}</p> : <><Button data-testid="evidence-preview" icon="file" disabled={disabled || !draft || !providerDisputeDetail || sellerEvidence || evidenceSent} loading={busy === 'evidence-preview'} onClick={previewEvidence}>Prepare evidence request (preview)</Button><Button data-testid="evidence-submit" icon={evidenceSubmitReady ? 'arrow' : 'lock'} tone={evidenceSubmitReady ? 'blue' : 'ghost'} aria-describedby={evidenceLock ? 'evidence-lock-reason' : undefined} disabled={disabled || !evidenceSubmitReady} loading={busy === 'evidence-submit'} onClick={() => setSendConfirm('evidence')} title="Requires PAYGUARD_PAYPAL_DISPUTE_SUBMIT=enabled, a Sandbox connection and a recorded local approval">Submit to PayPal Sandbox (test)</Button><LockReason testId="evidence-lock-reason" reason={evidenceLock} /><span className="text-dim">{hosted ? 'Test submission to the author\'s Sandbox test dispute: one send per dispute and per visit, at most 2 sends per address per day.' : 'Test submission. No real dispute is affected.'}</span>{itemNotReceived && !hosted && <><Button data-testid="tracking-preview" icon="file" disabled={disabled || !draft || !providerDisputeDetail} loading={busy === 'tracking-preview'} waiting={waitLeft('tracking-preview') > 0} onClick={previewTracking}>Preview tracking for PayPal</Button><Button data-testid="tracking-submit" icon={trackingSubmitReady ? 'arrow' : 'lock'} tone={trackingSendTone} aria-describedby={trackingLock ? 'tracking-lock-reason' : undefined} disabled={disabled || !trackingSubmitReady} loading={busy === 'tracking-submit'} onClick={() => setSendConfirm('tracking')} title="Requires PAYGUARD_PAYPAL_TRACKING_SUBMIT=enabled, a Sandbox connection and a recorded local approval">Send tracking to PayPal Sandbox (test)</Button><LockReason testId="tracking-lock-reason" reason={trackingLock} /></>}</>}</div>
            {(!hosted || sandboxSend) && <SendGuardSummary guard={(trackingPreview || evidencePreview)?.send_guard} detail={providerDisputeDetail} caseItem={caseItem} boundTo={boundTo} sentTo={sentTo} block={evidencePreview || trackingPreview ? (evidencePreview ? evidenceBlock : trackingBlock) : evidenceRefusal || trackingRefusal || sendGuardBlock(null, providerDisputeDetail, caseItem, boundTo, sentTo)} />}
            {sendConfirm && !(sendConfirm === 'evidence' && sellerEvidence) && <SendConfirmDialog kind={sendConfirm} detail={providerDisputeDetail} caseRef={caseItem?.case_ref} caseAmount={caseItem?.dispute_amount}
              returnFocus={[`[data-testid="${sendConfirm}-submit"]`, `[data-testid="phone-action-${sendConfirm}-submit"]`]}
              guard={(sendConfirm === 'tracking' ? trackingPreview : evidencePreview)?.send_guard}
              previewDisputeId={(sendConfirm === 'tracking' ? trackingPreview : evidencePreview)?.dispute_id}
              item={sendItemText(sendConfirm, sendConfirm === 'tracking' ? trackingPreview : evidencePreview)}
              onCancel={() => setSendConfirm(null)} onRecheck={() => recheckSend(sendConfirm)} onSend={() => confirmSend(sendConfirm)} />}
            {/* (round2 X, B 6a/6d) A stamp restored from this tab's storage says so; it is drawn only after the fresh read-back confirmed it. */}
            {restoredSend && !restoredSend.confirmed && restoredSend.dispute_id === providerDisputeDetail?.dispute_id && !evidenceSent && <p className="send-restored-note" data-testid="send-restored-note" role="status">{keptSendText(restoredSend)}. PayPal does not report this dispute under review, so it is not shown as submitted.</p>}
            {evidencePreview?.external_send === 'SUBMITTED' && <div className="send-receipt-big" data-testid="send-receipt" role="status"><strong>SUBMITTED to PayPal Sandbox</strong>{keptReceipt && <span data-testid="send-receipt-kept">{keptSendText(restoredSend)}</span>}<span data-testid="send-receipt-debug-id">PayPal-Debug-Id{keptReceipt ? ' (from that send, kept in this tab)' : ''}: {evidencePreview.paypal_debug_id || 'not returned'}</span><span data-testid="send-receipt-readback">{sendReadback === null ? 'Reading the dispute back…' : sendReadback.status ? `Read back: ${operatorLabel(sendReadback.status)}${sendReadback.debug ? ` · PayPal-Debug-Id ${sendReadback.debug}` : ''}` : 'Read-back unavailable; open the dispute again to check.'}</span><small>Dispute {displayDisputeId(evidencePreview.dispute_id)} · Sandbox test data · PayPal decides the case.</small></div>}
            {evidencePreview && <div className="evidence-preview" data-testid="evidence-preview-result"><div className="ai-brief-badges"><Badge tone={evidencePreview.external_send === 'SUBMITTED' ? 'green' : 'amber'}>{operatorLabel(evidencePreview.external_send)}</Badge><Badge tone="muted">{evidencePreview.data_source_label} data</Badge></div>{!evidenceSent && evidencePreview.paypal_debug_id && <p className="evidence-debug-id" data-testid="evidence-debug-id">PayPal-Debug-Id: {evidencePreview.paypal_debug_id}</p>}<ul>{evidencePreview.files.map((part) => <li key={part.name}>{part.name}: {part.filename} · {part.content_type} · {part.byte_length} bytes (file bytes stay on the server)</li>)}</ul>{evidencePreview.sent_files && evidencePreview.sent_files.map((file, index) => <p className="evidence-debug-id" key={index} data-testid="evidence-sent-sha256">Sent file SHA-256 (plain hash of the file's bytes): {file.sha256}</p>)}{evidenceSent ? (evidencePreview.sent_files?.length > 0 && <p className="text-dim" data-testid="evidence-fingerprint-note">{FINGERPRINT_NOTE}</p>) : <p className="text-dim">Tracking numbers are masked in this preview. Submit flag: {evidencePreview.submit_flag_enabled ? 'enabled' : 'off'}. A person reviews before any submission.</p>}</div>}
            {trackingPreview && <div className="evidence-preview tracking-preview" data-testid="tracking-preview-result"><div className="ai-brief-badges"><Badge tone={trackingPreview.external_send === 'SUBMITTED' ? 'green' : 'amber'}>{operatorLabel(trackingPreview.external_send)}</Badge><Badge tone="muted">{trackingPreview.data_source_label} data</Badge></div><dl className="approval-payload-list"><div><dt>Request</dt><dd>{trackingPreview.method} {trackingPreview.path}</dd></div>{trackingPreview.body.trackers.map((row) => <div key={`${row.transaction_id}-${row.tracking_number}`}><dt>Tracker (masked)</dt><dd data-testid="tracking-preview-row">Transaction {row.transaction_id} · {row.carrier === 'OTHER' ? row.carrier_name_other : row.carrier} {row.tracking_number} · {row.status}</dd></div>)}<div><dt>File fingerprint (SHA-256)</dt><dd className="approval-payload-hash" data-testid="tracking-preview-sha256">{trackingPreview.payload_sha256 || '—'}</dd></div>{trackingPreview.paypal_debug_id && <div><dt>PayPal-Debug-Id</dt><dd>{trackingPreview.paypal_debug_id}</dd></div>}</dl><p className="text-dim">Transaction id and tracking number are masked in this preview; the server sends the originals only after every gate passes. Submit flag: {trackingPreview.submit_flag_enabled ? 'enabled' : 'off'}.</p></div>}
            {/* (r33 M1) One Technical details for the whole evidence area, collapsed and last: the send helper text and,
                once prepared, the evidence request (method, path, content type, input JSON) that had its own disclosure. */}
            {/* (r34 #13) Set apart at the very bottom of the send area, well below the preview and its Debug-Id line. */}
            <details className="technical-details" data-testid="evidence-technical-details"><summary>Technical details</summary><p>Builds the multipart POST /v1/customer/disputes/{'{id}'}/provide-evidence from the local draft. Select a dispute and prepare the evidence draft first. The send button stays disabled until the operator sets PAYGUARD_PAYPAL_DISPUTE_SUBMIT=enabled, the Sandbox is connected, a person has recorded the local approval and a preview has been prepared.</p>{evidencePreview && <div className="evidence-technical-request" data-testid="evidence-technical-request"><div className="ai-brief-badges"><Badge tone="blue">{evidencePreview.method} {evidencePreview.path}</Badge><Badge tone="muted">{evidencePreview.content_type}</Badge></div><pre>{JSON.stringify(evidencePreview.input, null, 2)}</pre></div>}
              {providerDisputeDetail && <><h4 className="provider-dispute-detail-title">Selected dispute, as PayPal returned it</h4><dl className="provider-dispute-detail" data-testid="provider-dispute-detail">{[
                ['Dispute', displayDisputeId(providerDisputeDetail.dispute_id)],
                ['Source', `${providerDisputeDetail.data_source_label} · GET /v1/customer/disputes/{id}`],
                ['Reason', operatorLabel(providerDisputeDetail.reason)],
                ['Status', `${operatorLabel(providerDisputeDetail.status)} · ${operatorLabel(providerDisputeDetail.dispute_life_cycle_stage)}`],
                ['Amount', `${providerDisputeDetail.dispute_amount.value} ${providerDisputeDetail.dispute_amount.currency_code}`],
                ['Transactions', providerDisputeDetail.disputed_transactions.map((row) => `${row.seller_transaction_id} (${operatorLabel(row.transaction_status, 'status not stated')})`).join(', ') || 'None returned'],
                ['Evidence requests', providerDisputeDetail.evidences.map((row) => `${operatorLabel(row.evidence_type, row.evidence_type)} · ${operatorLabel(row.source, row.source)}`).join('; ') || 'None returned'],
                ['Provider submission', sellerEvidence ? SELLER_EVIDENCE_TEXT : operatorLabel(providerDisputeDetail.provider_submission)],
                ['Seller Protection', sellerProtectionLabel(providerDisputeDetail)],
                ...(providerDisputeDetail.paypal_debug_id ? [['PayPal-Debug-Id', `${providerDisputeDetail.paypal_debug_id} (this read)`]] : []),
              ].map(([label, value]) => <div key={label}><dt>{label}</dt><dd>{value}</dd></div>)}</dl></>}
            </details>
          </div>
        </details>
        <StepSection id="evidence-board" title="Evidence deadline board" subtitle="Deadlines on a timeline" icon="clock" open={boardOpen} onToggle={setBoardExpanded} testId="optional-toggle-evidence-board">{boardOpen ? <Suspense fallback={<div className="analytics-loading" role="status"><span className="spinner" />Loading the evidence deadline board.</div>}><EvidenceBoard disputes={state?.disputes} drafts={boardDraftsForState} sandbox={providerDisputes?.source === 'paypal_sandbox' ? providerDisputes.items : null} /></Suspense> : null}</StepSection>
        </div><aside className="stage-side">
        <GuideLive key={`dispute-${sessionRef.current?.session_id || 'no-session'}`} scenario="dispute" session={sessionRef.current} Disclosure={StepSection} Badge={Badge} onChooser={setGuideChooser} onOpenItems={setGuideOpenItems} request={guideRequest} onSessionExpired={panelSessionExpired} />
        <StepMore id="disputes"><StepSection id="guide-replay" title="Guided gap filling: examples" subtitle="Replayed examples, never a live model call" icon="layers" open={replayExpanded} onToggle={setReplayExpanded} testId="optional-toggle-replay">{replayExpanded ? <Suspense fallback={<div className="analytics-loading" role="status"><span className="spinner" />Loading the replay examples.</div>}><GuideReplay /></Suspense> : null}</StepSection>
        <StepSection id="sources-dispute_mediation" title="Sources, policy check, and AI brief" subtitle="Official sources, demo claim check, AI summary, technical details" icon="link" open={Boolean(sourcesOpen.dispute_mediation)} onToggle={(next) => setSourcesOpen((current) => ({ ...current, dispute_mediation: next }))} testId="sources-toggle-dispute_mediation">
          <SecondaryStageTabs stage="dispute_mediation" activeTab={openSecondary.dispute_mediation} onSelectTab={toggleSecondary} referenceProps={referenceProps} aiAvailable={Boolean(draft) && caseItem?.reason === 'INR' && draft?.evidence?.reason === 'INR' && draft?.routing?.overall_state === 'READY_FOR_LOCAL_REVIEW' && !draft?.review_reasons?.includes('unsupported_reason') && !disabled && !busy && !aiBusyStage} brief={aiBriefs.dispute_mediation} notice={aiNotices.dispute_mediation} aiLoading={aiBusyStage === 'dispute_mediation'} onGenerateAi={generateAiBrief} hosted={hosted} techContent={<div className="velocity-details"><p>Dispute readback uses GET /v1/customer/disputes and GET /v1/customer/disputes/{'{id}'}; evidence preview prepares multipart POST /v1/customer/disputes/{'{id}'}/provide-evidence.</p>{draft?.routing && <p data-testid="dispute-route-server">Server routing: {operatorLabel(draft.routing.overall_state)} · next options: {operatorLabels(draft.routing.available_actions).join(', ') || 'None'} · due {utcLabel(draft.routing.seller_response_due_date)}</p>}<span>{state?.policy_version || 'POLICY —'}</span></div>} />
        </StepSection><LimitsDrawer id="disputes"><p className="text-dim" data-testid="reviewer-identity-note">Demo only: there is no sign-in, so the reviewer is not identified.</p><div className="case-note"><Icon name="shield" size={15} /><p>Delivery records help review a case; they do not decide it.</p></div><p className="review-warning review-warning-short"><strong>Internal review only.</strong> This ZIP is not a PayPal attachment. Nothing was sent; a person checks it first.</p><p className="review-warning" data-testid="internal-review-zip-boundary"><strong>INTERNAL REVIEW ONLY</strong> — This synthetic, pseudonymized preparation package is not a PayPal-supported attachment. Required fields present does not prove authenticity, sufficiency, eligibility, completeness, or outcome. PayPal or the external issuer keeps final authority, and nothing was submitted.</p></LimitsDrawer></StepMore>
        </aside></div>
      </StageAccordion>

      <OptionalDisclosure id="analytics" title="Merchant Evidence Buffer" subtitle="Review all orders in one table" icon="layers" badge={<Badge tone="blue">OPTIONAL</Badge>} open={analyticsExpanded} onToggle={setAnalyticsExpanded} testId="optional-toggle-analytics">{analyticsOpen ? <Suspense fallback={<div className="analytics-loading" role="status"><span className="spinner" />Loading the isolated analytics workspace.</div>}><AnalyticsDashboard aup={aup} state={state} /></Suspense> : <div className="analytics-launch-card"><div className="analytics-launch-copy"><span className="meta-label">OPTIONAL</span><strong>Review all orders in one table</strong><p>See every order in one table, with filters and a read-only guide.</p><div className="analytics-launch-tags"><span>Quick filtering</span><span>Human review</span></div></div><Button data-testid="analytics-launch" icon="layers" tone="blue" disabled={!state} onClick={() => setAnalyticsOpen(true)}>Open all orders</Button></div>}</OptionalDisclosure>

      <OptionalDisclosure id="activity" title="Session activity" subtitle={`${state?.activity?.length || 0} local events · maximum 30`} icon="clock" open={activityExpanded} onToggle={setActivityExpanded} testId="optional-toggle-activity"><section className="activity-panel" aria-label="Demo activity log"><ol>{state?.activity?.length ? state.activity.slice().reverse().map((event) => <li key={event.id}><span className="activity-dot" /><time>{dateLabel(event.at)}</time><strong>{event.label}</strong><Badge tone="muted">{event.source}</Badge></li>) : <li className="activity-empty">No activity yet. Demo actions will appear here.</li>}</ol></section></OptionalDisclosure>
      <footer><details className="sponsor-map" data-testid="sponsor-map"><summary>Sponsor map</summary><ul>{SPONSOR_MAP.map((entry) => <li key={entry.name}><strong>{entry.name}</strong> <span>{entry.what}</span> <a href={sponsorHref(entry)} data-testid={`sponsor-link-${entry.name.replace(/\s+/gu, '-')}`}>{entry.proof ? 'Proof rows' : 'Where it runs'}</a></li>)}</ul></details><span><Icon name="shield" size={15} /> TradeGlot <span className="footer-divider">/</span> {hosted ? <span data-testid="hosted-note-footer">Hosted demo</span> : 'Local prototype'}</span><a className="footer-download-demo" href="https://github.com/jiarong0423/payguard-ai/releases/download/demo-package-20261109/tradeglot-demo.zip" target="_blank" rel="noopener noreferrer" title="Same demo, one command, no keys." aria-label="Download the demo (11 MB). Same demo, one command, no keys." data-testid="footer-download-demo"><svg className="download-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.9" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M12 4v10.5" /><path d="m7.5 10.5 4.5 4.5 4.5-4.5" /><path d="M5 19.25h14" /></svg><span>Download the demo (11 MB)</span></a><span className="footer-independent" data-testid="footer-independent">TradeGlot is an independent hackathon demo. Not affiliated with or endorsed by PayPal.</span><span>Demo data · you decide · nothing is sent without your click</span></footer>
    </main>
    {phoneAction && <div className={`phone-action-bar${phoneReason ? ' has-reason' : ''}`} ref={phoneBarRef} data-testid="phone-action-bar" role="region" aria-label="Current step action" inert={warningOpen || draftConfirm || resetConfirm || sendConfirm ? true : undefined}><Button data-testid={`phone-action-${phoneAction.key}`} icon={phoneAction.icon} tone="blue" disabled={phoneAction.disabled || phoneSendHeld} loading={phoneAction.loading} blocked={phoneAction.blocked} waiting={phoneAction.waiting} aria-describedby={phoneAction.blocked ? 'description-note' : undefined} onClick={phoneActionClick}>{phoneAction.label}</Button>{phoneReason && <small className="phone-action-reason" data-testid="phone-action-reason" title={phoneReason}>{phoneReason}</small>}</div>}
    {warningOpen && <div className="aup-warning-backdrop" onMouseDown={holdWarningFocus}><div ref={warningRef} className="aup-warning-dialog" role="dialog" aria-modal="true" aria-labelledby="aup-warning-title" aria-describedby="aup-warning-copy" data-testid="aup-warning-dialog" onKeyDown={warningKeys} tabIndex={-1}>
      <Badge tone="amber">Second reminder · Needs review</Badge>
      <h2 id="aup-warning-title">Review the actual goods or activity before continuing</h2>
      <p id="aup-warning-copy">The description matched a demo rule. This is a reminder only. Read the official policy, then acknowledge to continue.</p>
      <p>Acknowledging is not a compliance approval, a PayPal review or an invoice send. If you change the description, check again.</p>
      <a data-testid="aup-warning-policy-link" href={AUP_POLICY_URL} target="_blank" rel="noopener noreferrer">Review the PayPal US Acceptable Use Policy</a>
      <div className="aup-warning-actions">
        <Button data-testid="aup-return-to-edit" disabled={Boolean(busy)} onClick={() => chooseWarning('RETURN_TO_EDIT')}>Return to edit</Button>
        <Button data-testid="aup-cancel" disabled={Boolean(busy)} onClick={() => chooseWarning('CANCEL')}>Cancel flow</Button>
        <Button data-testid="aup-acknowledge" tone="blue" loading={busy === 'aup-choice'} disabled={Boolean(busy)} onClick={() => chooseWarning('ACKNOWLEDGE_AND_CONTINUE')}>Acknowledge and continue</Button>
      </div>
    </div></div>}
  </div>;
}

// (optimise r24) WCAG 2.2.1 timing: the policy result expires at the server's expires_at (about two minutes). In its last 30
// seconds this warns with a countdown and offers "Keep this result". There is no server endpoint that extends an
// evaluation, so Keep runs the same check again, and only while the description is unchanged; that new check counts
// against the server's 5 open policy checks per 2 minutes, which the message says.
const AUP_WARN_MS = 30000;
// (r32 J4 P1-1) A second Run Policy Check press runs a new check (and a new 2-minute window) only this long after the
// shown one; a quicker repeat is treated as a double tap. At most 4 renewals fit in the server's 5 checks per 2 minutes.
const AUP_RENEW_AFTER_MS = 30000;
// (r32 J4 P2-3) "Check valid for 1:12 more" next to the result, so the operator can read the 2-minute window off the
// screen. The ticking time is aria-hidden (the result is a live region); a screen reader gets one fixed sentence.
function AupValidFor({ expiresAt }) {
  const end = Date.parse(expiresAt || '');
  const [now, setNow] = useState(() => Date.now());
  useEffect(() => {
    if (!Number.isFinite(end)) return undefined;
    const interval = window.setInterval(() => { const at = Date.now(); setNow(at); if (at >= end) window.clearInterval(interval); }, 1000);
    return () => window.clearInterval(interval);
  }, [end]);
  const left = Math.ceil((end - now) / 1000);
  if (!Number.isFinite(end) || left <= 0) return null;
  return <p className="aup-valid-for text-dim" data-testid="aup-valid-for"><Icon name="clock" size={14} /><span aria-hidden="true">Check valid for {Math.floor(left / 60)}:{String(left % 60).padStart(2, '0')} more</span><span className="sr-only">This check is valid for 2 minutes.</span></p>;
}
function AupExpiryWarning({ expiresAt, onKeep, blocked, loading, productConfirmed }) {
  const end = Date.parse(expiresAt || '');
  const [now, setNow] = useState(() => Date.now());
  useEffect(() => {
    if (!Number.isFinite(end)) return undefined;
    let interval = 0;
    const start = () => {
      setNow(Date.now());
      interval = window.setInterval(() => { const at = Date.now(); setNow(at); if (at >= end) window.clearInterval(interval); }, 1000);
    };
    const timer = window.setTimeout(start, Math.max(0, end - AUP_WARN_MS - Date.now()));
    return () => { window.clearTimeout(timer); window.clearInterval(interval); };
  }, [end]);
  const left = Math.ceil((end - now) / 1000);
  if (!Number.isFinite(end) || left > AUP_WARN_MS / 1000 || left <= 0) return null;
  // The seconds are hidden from screen readers so the status is announced once, not every second.
  return <div className="aup-expiry" data-testid="aup-expiry-warning" role="status">
    <p><strong>This result expires in <span aria-hidden="true" data-testid="aup-expiry-seconds">{left} s</span><span className="sr-only">less than 30 seconds</span>.</strong>{' '}
      Keep it to run the same check again on this unchanged description. That uses one of the 5 policy checks allowed per 2 minutes.{productConfirmed ? ' The product card you confirmed is asked again after the new check.' : ''}</p>
    <Button data-testid="aup-keep-result" icon="clock" onClick={onKeep} blocked={blocked} loading={loading}>Keep this result</Button>
  </div>;
}

// (optimise r24) Phones: 24 baseline hours plus the spike hour made the spike bar a hairline. Under 641 px the chart
// gets the last SPIKE_PHONE_BASELINE_HOURS baseline hours before the spike window (about 11 bars with a one-hour
// window); the velocity numbers above the chart are unchanged.
const SPIKE_PHONE_BASELINE_HOURS = 10;
function useNarrowScreen(query = '(max-width: 640px)') {
  const [narrow, setNarrow] = useState(() => typeof window !== 'undefined' && window.matchMedia(query).matches);
  useEffect(() => {
    const media = window.matchMedia(query);
    const update = () => setNarrow(media.matches);
    update();
    media.addEventListener('change', update);
    return () => media.removeEventListener('change', update);
  }, [query]);
  return narrow;
}
function phoneChartVelocity(velocity, narrow) {
  if (!velocity || !narrow) return velocity;
  const end = Date.parse(velocity.baseline_window_end || '');
  const start = Date.parse(velocity.baseline_window_start || '');
  if (!Number.isFinite(end) || !Number.isFinite(start)) return velocity;
  const trimmed = Math.max(start, end - SPIKE_PHONE_BASELINE_HOURS * 3600 * 1000);
  return trimmed === start ? velocity : { ...velocity, baseline_window_start: new Date(trimmed).toISOString() };
}

// (optimise r24) Phones: the chart's own legend pages ("1 / 2") at 375 px, so the three marks are listed once here,
// unpaginated. Its colours are the chart's (charts/velocityChartData.js BASELINE_FILL, SPIKE_FILL, REVIEW_STROKE).
function PhoneChartLegend() {
  return <ul className="phone-chart-legend" data-testid="velocity-phone-legend" aria-label="Chart legend">
    <li><span className="phone-legend-mark is-usual" aria-hidden="true" />Usual rate</li>
    <li><span className="phone-legend-mark is-spike" aria-hidden="true" />Spike window · orders</li>
    <li><span className="phone-legend-mark is-flag" aria-hidden="true" />Above the review line</li>
    <li><span className="phone-legend-mark is-review" aria-hidden="true" />Review threshold</li>
  </ul>;
}

// (optimise r24) Under the spike chart: the signal, which order records in the synthetic data back it, which are
// missing, and the published reserve case it relates to. Counting only; no prediction of any PayPal action.
const RESERVE_CASE_URL = 'https://www.financial-ombudsman.org.uk/decision/DRN-5706769.pdf';
function SpikeRecordsCard({ velocity, transactions }) {
  if (!velocity?.transaction_count) return null;
  const start = Date.parse(velocity.window_start || '');
  const end = Date.parse(velocity.window_end || '');
  const inWindow = (Array.isArray(transactions) ? transactions : []).filter((row) => {
    const at = Date.parse(row?.occurred_at || '');
    return Number.isFinite(at) && at > start && at <= end;
  });
  const count = inWindow.length;
  const withCapture = inWindow.filter((row) => row.order_id && row.amount && row.occurred_at).length;
  // The synthetic burst orders carry order id, amount, currency and capture time only (backend store.py burst rows).
  const has = (field) => inWindow.filter((row) => row && row[field] !== undefined && row[field] !== null && row[field] !== '').length;
  const missing = [['Tracking numbers', has('tracking_number')], ['Delivery confirmations', has('delivered_at')], ['Customer messages', has('messages')]];
  return <section className="spike-records" data-testid="spike-records" aria-label="Signal, records and missing records">
    <div className="spike-records-row" data-testid="spike-records-signal"><span className="meta-label">Signal</span>
      <p>{velocity.alert ? `Sales in the last ${velocity.window_hours} h are ${velocity.ratio}× the usual rate (review line ${velocity.threshold}×).` : `Sales in the last ${velocity.window_hours} h are ${velocity.ratio}× the usual rate, under the review line of ${velocity.threshold}×.`}</p></div>
    <div className="spike-records-row" data-testid="spike-records-backed"><span className="meta-label">Records that back it</span>
      <p>{withCapture} of {count} orders in the window have an order record with amount and capture time.</p></div>
    <div className="spike-records-row" data-testid="spike-records-missing"><span className="meta-label">Missing</span>
      {/* (r34 #8) Counted as missing, not present: "0 of 50" read as "none missing" when all 50 lacked the record. */}
      <ul>{missing.map(([label, present]) => <li key={label}>{label}: missing in {count - present} of {count} orders</li>)}</ul></div>
    <p className="spike-records-case" data-testid="spike-records-case">Related published case: <a href={RESERVE_CASE_URL} target="_blank" rel="noopener noreferrer">DRN-5706769 ↗</a>, a new business account with a sharp rise in sales had part of its funds held and a 15% rolling reserve applied.</p>
  </section>;
}

// (r25 send guard) Safeguards against sending to the wrong dispute. The server holds every rule (two-way case <->
// dispute binding, fresh read, account identity, one send per approval); the console shows the same facts side by
// side, disables a send that would be refused, and asks twice before any real send (submit: true).
const SEND_HOLD_SECONDS = 3;
// (rehearsal 2026-11-04) The draft line shows the last 4 characters so the video can match the PayPal Sandbox
// Invoices page; the full id stays off screen like the other raw ids.
const maskInvoiceId = (value) => (typeof value === 'string' && /^INV2-[A-Z0-9-]{8,64}$/.test(value) ? `INV2-…${value.slice(-4)}` : '…');
const maskDisputeId = (value) => (typeof value === 'string' && value.length > 8 ? `${value.slice(0, 5)}…${value.slice(-2)}` : '…');
// (2026-11-11) maskDisputeId is for comparisons only (pairing, lock, sentByCaseRef). What the screen shows goes through
// displayDisputeId (./disputeDisplay.js): a code the server already masked (PP-R-VAF-XXXX7877, hosted) as is, a raw id in
// the short form. tests/frontend_dispute_display_map.mjs keeps the two apart.
const ACCOUNT_LINES = {
  account_identity_unknown: 'TradeGlot cannot confirm which PayPal Sandbox account is connected, so it will not send.',
  dispute_not_this_account: 'This dispute belongs to a different PayPal account than the connected Sandbox account.',
  dispute_detail_required: 'Open this dispute\'s details first, so its seller account can be checked.',
  // (r34 E1 P1-1) The dispute itself cannot take evidence now; the account may still match.
  seller_evidence_already_submitted: 'PayPal already has seller evidence for this dispute, so TradeGlot will not send more.',
  dispute_not_awaiting_seller: 'This dispute is not waiting for the seller, so PayPal would not take evidence now.',
  dispute_evidence_not_offered: 'PayPal does not offer evidence upload for this dispute right now.',
};
const sameMoney = (left, right) => Boolean(left && right) && left.currency_code === right.currency_code && Number(left.value) === Number(right.value);

// (fix r1 U4) Two different values by construction (backend/app/paypal_disputes.py evidence_payload_sha256 and the
// send's sent_files): the preview's is an HMAC-SHA256 under a per-session key over the whole request, the receipt's is
// the plain SHA-256 of one file's bytes. They can never be equal, so each is labelled for what it covers.
const FINGERPRINT_NOTE = 'The request fingerprint shown before sending is a session-keyed hash of the whole request; this is the plain hash of the file alone, so the two differ by design.';

// One plain line saying why a send is held, or null when the case and the dispute agree.
// (r34 #3) "already sent" only after a real send from this page (`sentTo`); a pairing made by a preview says so and
// names Reset demo, which clears it on the server.
// (round2 X, B 2c/5a) Every identity check compares full dispute ids as the API returned them (the hosted code, or the
// raw local id): `boundTo`, `sentTo` and `previewId` (the preview's own dispute_id). The 5+2 short form is shared by
// look-alikes (PP-R-AXM-XXXX0001 / PP-R-WAH-XXXX0001), so it is never the key; the server's short form can only add a
// hold. The lines name the disputes through displayDisputeId.
function sendGuardBlock(guard, detail, caseItem, boundTo, sentTo = null, previewId = null) {
  if (!detail) return 'Select a PayPal dispute first.';
  const here = detail.dispute_id;
  const bound = boundTo || sentTo;
  if (bound && bound !== here) return sentTo === bound ? `This case was already sent to ${displayDisputeId(bound)}; it cannot also go to ${displayDisputeId(here)}.`
    : `Paired with ${displayDisputeId(bound)} (preview only). Reset demo to pair it with another dispute.`;
  if (!guard) return 'Prepare the preview for this dispute first.';
  if (typeof previewId !== 'string' || previewId !== here) return 'The preview is for another dispute; prepare it again for this one.';
  if (guard.bound_dispute_masked && guard.bound_dispute_masked !== maskDisputeId(here)) return 'The server reports this case paired with another dispute. Reset demo to pair it with this one.';
  if (guard.case_reason !== detail.reason) return `The case reason (${operatorLabel(guard.case_reason, 'not stated')}) does not match this dispute (${operatorLabel(detail.reason)}).`;
  const expected = detail.source === 'synthetic_fixture' ? caseItem?.dispute_amount : guard.dispute_amount;
  if (!expected || expected.currency_code !== detail.dispute_amount.currency_code) return `The currency does not match: the case expects ${expected?.currency_code || 'no currency'}, the dispute is in ${detail.dispute_amount.currency_code}.`;
  if (!sameMoney(expected, detail.dispute_amount)) return `The amount does not match: the case expects ${expected.value} ${expected.currency_code}, the dispute shows ${detail.dispute_amount.value} ${detail.dispute_amount.currency_code}.`;
  if (guard.send_refusal) return ACCOUNT_LINES[guard.send_refusal];
  return null;
}

// What is being sent: evidence files (and tracking rows), or the carrier and masked tracking number.
function sendItemText(kind, preview) {
  if (!preview) return 'Nothing prepared yet.';
  if (kind === 'tracking') {
    const tracker = preview.body.trackers[0];
    return `Tracking: ${tracker.carrier === 'OTHER' ? tracker.carrier_name_other : tracker.carrier} ${tracker.tracking_number}`;
  }
  const rows = preview.input.evidences.flatMap((row) => row.evidence_info.tracking_info);
  const files = preview.files.map((part) => part.filename).join(', ') || 'no files';
  return `Evidence: ${preview.input.evidences.map((row) => operatorLabel(row.evidence_type, row.evidence_type)).join(', ')}; files: ${files}; ${rows.length} tracking row${rows.length === 1 ? '' : 's'} (masked)`;
}

// Case on the left, PayPal dispute on the right, plus the binding and the account check.
function SendGuardSummary({ guard, detail, caseItem, boundTo, sentTo = null, block }) {
  if (!detail) return null;
  const amount = detail.dispute_amount;
  return <div className="send-guard" data-testid="send-guard">
    <div className="send-guard-side" data-testid="send-guard-case"><span className="send-guard-label">From case</span>
      <strong>{caseItem?.case_ref || '—'}</strong><span>{operatorLabel(guard?.case_reason || caseItem?.reason, 'Reason not stated')}</span></div>
    <Icon name="link" size={16} />
    <div className="send-guard-side" data-testid="send-guard-dispute"><span className="send-guard-label">To PayPal dispute</span>
      <strong>{displayDisputeId(detail.dispute_id)}</strong><span>{operatorLabel(detail.reason)} · {amount.value} {amount.currency_code}</span></div>
    {(boundTo || sentTo) && <p className="send-guard-bound" data-testid="send-guard-bound">{sentTo && sentTo === (boundTo || sentTo) ? `This case was sent to ${displayDisputeId(sentTo)}.` : `This case is paired with ${displayDisputeId(boundTo)} (preview only).`}</p>}
    {guard && <p className="send-guard-account" data-testid="send-guard-account">Sending as: Sandbox account {guard.sending_account_masked || 'unknown'} · dispute seller: {guard.dispute_seller_masked || 'unknown'}</p>}
    {block && <p className="send-guard-block" role="status" data-testid="send-guard-block"><Icon name="alert" size={15} />{block}</p>}
  </div>;
}

// Two steps before a real send: (1) the summary and a tick, "Continue"; (2) "This sends to PayPal and cannot be undone
// here.", "Send to PayPal" held for SEND_HOLD_SECONDS with a visible countdown. Back and Escape cancel; focus stays
// inside while open and returns to the trigger when it closes.
function SendConfirmDialog({ kind, guard, detail, previewDisputeId = null, caseRef, caseAmount = null, item, returnFocus = [], onCancel, onRecheck, onSend }) {
  const [step, setStep] = useState(1);
  const [checked, setChecked] = useState(false);
  const [left, setLeft] = useState(SEND_HOLD_SECONDS);
  const [sending, setSending] = useState(false);
  const [checking, setChecking] = useState(false);
  const boxRef = useRef(null);
  useEffect(() => {
    const trigger = document.activeElement;
    boxRef.current?.querySelector('input, button')?.focus();
    return () => restoreFocus(trigger, returnFocus);
  }, []); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => {
    if (step !== 2 || left <= 0) return undefined;
    const timer = setTimeout(() => setLeft((value) => value - 1), 1000);
    return () => clearTimeout(timer);
  }, [step, left]);
  useEffect(() => { if (step === 2) boxRef.current?.querySelector('[data-testid="send-confirm-back"]')?.focus(); }, [step]);
  const keyDown = (event) => {
    if (event.key === 'Escape') { event.preventDefault(); onCancel(); return; }
    if (event.key !== 'Tab') return;
    const focusable = [...(boxRef.current?.querySelectorAll('input:not([disabled]), button:not([disabled])') || [])];
    if (!focusable.length) return;
    const first = focusable[0]; const last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
    else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
  };
  const proceed = async () => {
    setChecking(true);
    const fresh = await onRecheck();
    setChecking(false);
    if (fresh) { setLeft(SEND_HOLD_SECONDS); setStep(2); }
  };
  const send = async () => { if (sending) return; setSending(true); await onSend(); };
  const title = kind === 'tracking' ? 'Send tracking to PayPal Sandbox' : 'Send evidence to PayPal Sandbox';
  // (r32 J5 P3-2, J4 P2-2) Drawn on document.body: inside the Disputes <details> a closed parent hid the fixed
  // dialog, and the body's muted paragraph colour turned the orange warning grey.
  return createPortal(<div className="send-confirm-backdrop" data-testid="send-confirm-backdrop">
    <div className="send-confirm" ref={boxRef} role="dialog" aria-modal="true" aria-labelledby="send-confirm-title" data-testid="send-confirm" onKeyDown={keyDown}>
      <h3 id="send-confirm-title">{title}</h3>
      {step === 1 ? <>
        <dl className="send-confirm-summary" data-testid="send-confirm-summary">
          <div><dt>Case</dt><dd data-testid="send-confirm-case">{caseRef} · {operatorLabel(guard?.case_reason, 'Reason not stated')}</dd></div>
          <div><dt>PayPal dispute</dt><dd data-testid="send-confirm-dispute">{displayDisputeId(typeof previewDisputeId === 'string' && previewDisputeId === detail?.dispute_id ? detail.dispute_id : guard?.dispute_masked)}</dd></div>
          {/* (red team A 2026-11-04 P2) The masked id keeps 2 characters; amount and opening date tell two look-alike disputes apart. */}
          {/* (r34 #6) The case's own amount beside PayPal's, so a 48 USD case against a 158 TWD dispute is visible here. */}
          <div><dt>Case amount</dt><dd data-testid="send-confirm-case-amount">{caseAmount ? `${caseAmount.value} ${caseAmount.currency_code}` : '—'}</dd></div>
          <div><dt>Dispute amount</dt><dd data-testid="send-confirm-amount">{detail?.dispute_amount ? `${detail.dispute_amount.value} ${detail.dispute_amount.currency_code}` : '—'}</dd></div>
          <div><dt>Opened</dt><dd data-testid="send-confirm-opened">{typeof detail?.create_time === 'string' ? dateLabel(detail.create_time) : '—'}</dd></div>
          <div><dt>Account</dt><dd data-testid="send-confirm-account">Sending as: Sandbox account {guard?.sending_account_masked || 'unknown'} · dispute seller: {guard?.dispute_seller_masked || 'unknown'}</dd></div>
          <div><dt>Item</dt><dd data-testid="send-confirm-item">{item}</dd></div>
        </dl>
        <label className="send-confirm-check"><input type="checkbox" data-testid="send-confirm-tick" checked={checked} onChange={(event) => setChecked(event.target.checked)} /> I checked this is the right dispute</label>
        <div className="send-confirm-actions">
          <Button data-testid="send-confirm-cancel" tone="ghost" onClick={onCancel}>Back</Button>
          <Button data-testid="send-confirm-continue" className="button-confirm-continue" icon="arrow" disabled={!checked || checking || guard?.account_status !== 'MATCH'} loading={checking} onClick={proceed}>Continue</Button>
        </div>
      </> : <>
        <p className="send-confirm-warning" data-testid="send-confirm-warning"><Icon name="alert" size={16} />This sends to PayPal and cannot be undone here.</p>
        <p className="send-confirm-countdown" aria-live="polite" data-testid="send-confirm-countdown">{left > 0 ? `Send is available in ${left} second${left === 1 ? '' : 's'}.` : 'You can send now.'}</p>
        <div className="send-confirm-actions">
          <Button data-testid="send-confirm-back" tone="ghost" onClick={onCancel}>Back</Button>
          <Button data-testid="send-confirm-send" className={`button-confirm-send${left > 0 ? ' is-holding' : ''}`} icon={left > 0 ? 'lock' : 'arrow'} disabled={left > 0 || sending} loading={sending} onClick={send}>Send to PayPal{left > 0 ? ` (${left})` : ''}</Button>
        </div>
      </>}
    </div>
  </div>, document.body);
}

// (r31 J2 J4 J5 A4) One visible line under a locked primary action (lockReasons.js), not only the button's title,
// which touch screens never show and screen readers may skip on a disabled button.
// (r32 J4 a11y) The test id is also the element id, so the button it locks points at it with aria-describedby and a
// screen reader reads the reason with the button.
function LockReason({ reason, testId }) {
  if (!reason) return null;
  return <p className="lock-reason" id={testId} data-testid={testId}><Icon name="lock" size={14} /><span>{reason}</span></p>;
}

// (r32 J4 a11y) Focus goes back to the button that opened the dialog. Safari does not focus a clicked button, so
// document.activeElement at open time can be another element (after a local review it was the receipt); then, or
// when that element is gone or disabled, the first usable `returnFocus` selector (the opening button) gets focus.
function restoreFocus(trigger, returnFocus) {
  const usable = (element) => element && element.isConnected && !element.disabled && element.getClientRects().length > 0;
  const opener = returnFocus.some((selector) => trigger?.matches?.(selector)) && usable(trigger) ? trigger
    : returnFocus.map((selector) => document.querySelector(selector)).find(usable) || (usable(trigger) ? trigger : null);
  if (opener && typeof opener.focus === 'function') opener.focus();
}

// (foolproofing 2026-11-04) Shared dialog behaviour: focus moves inside, Tab stays inside, Escape cancels, focus
// returns to the trigger on close.
function useDialogFocus(boxRef, onCancel, returnFocus = []) {
  useEffect(() => {
    const trigger = document.activeElement;
    boxRef.current?.querySelector('input, button')?.focus();
    return () => restoreFocus(trigger, returnFocus);
  }, [boxRef]); // eslint-disable-line react-hooks/exhaustive-deps
  return (event) => {
    if (event.key === 'Escape') { event.preventDefault(); onCancel(); return; }
    if (event.key !== 'Tab') return;
    const focusable = [...(boxRef.current?.querySelectorAll('input:not([disabled]), button:not([disabled])') || [])];
    if (!focusable.length) return;
    const first = focusable[0]; const last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
    else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
  };
}

// (foolproofing 2026-11-04) The Sandbox invoice draft is a real PayPal write, so it gets the same two steps as a
// send: (1) what will be created and a tick, orange "Continue"; (2) green "Create draft" held for SEND_HOLD_SECONDS.
// (r31 J4 P1-2) `expired`: the policy result behind the draft ran out while the dialog was open. Either step is
// replaced by DRAFT_EXPIRED_TEXT and Back, so nothing can be created and the seller knows what to do next.
function DraftConfirmDialog({ description, amount, currency, route, expired = false, returnFocus = [], onCancel, onCreate }) {
  const [step, setStep] = useState(1);
  const [checked, setChecked] = useState(false);
  const [left, setLeft] = useState(SEND_HOLD_SECONDS);
  const [creating, setCreating] = useState(false);
  const boxRef = useRef(null);
  const keyDown = useDialogFocus(boxRef, onCancel, returnFocus);
  useEffect(() => {
    if (step !== 2 || left <= 0) return undefined;
    const timer = setTimeout(() => setLeft((value) => value - 1), 1000);
    return () => clearTimeout(timer);
  }, [step, left]);
  useEffect(() => { if (step === 2) boxRef.current?.querySelector('[data-testid="draft-confirm-back"]')?.focus(); }, [step]);
  // The focused Continue or Create goes away on expiry; focus stays inside the dialog, on Back.
  useEffect(() => { if (expired) boxRef.current?.querySelector('[data-testid="draft-confirm-expired-back"]')?.focus(); }, [expired]);
  const create = async () => { if (creating) return; setCreating(true); await onCreate(); };
  const shown = typeof description === 'string' && description.length > 120 ? `${description.slice(0, 117)}...` : description;
  // (r32 J5 P3) On document.body like the send dialog, so no ancestor's overflow or transform can clip it.
  return createPortal(<div className="send-confirm-backdrop" data-testid="draft-confirm-backdrop">
    <div className="send-confirm" ref={boxRef} role="dialog" aria-modal="true" aria-labelledby="draft-confirm-title" data-testid="draft-confirm" onKeyDown={keyDown}>
      <h3 id="draft-confirm-title">Create a PayPal Sandbox invoice draft</h3>
      {expired ? <>
        <p className="send-confirm-expired" role="alert" data-testid="draft-confirm-expired"><Icon name="clock" size={16} />{DRAFT_EXPIRED_TEXT}</p>
        <div className="send-confirm-actions">
          <Button data-testid="draft-confirm-expired-back" tone="ghost" onClick={onCancel}>Back</Button>
        </div>
      </> : step === 1 ? <>
        <dl className="send-confirm-summary" data-testid="draft-confirm-summary">
          <div><dt>Item</dt><dd data-testid="draft-confirm-description">{shown || '—'}</dd></div>
          <div><dt>Amount</dt><dd data-testid="draft-confirm-amount">{amount} {currency}</dd></div>
          <div><dt>Route</dt><dd data-testid="draft-confirm-route">{route || 'No country check run'}</dd></div>
          <div><dt>What happens</dt><dd>A draft is created in PayPal Sandbox. It is not sent to the buyer.</dd></div>
        </dl>
        <label className="send-confirm-check"><input type="checkbox" data-testid="draft-confirm-tick" checked={checked} onChange={(event) => setChecked(event.target.checked)} /> I checked the item and the amount</label>
        <div className="send-confirm-actions">
          <Button data-testid="draft-confirm-cancel" tone="ghost" onClick={onCancel}>Back</Button>
          <Button data-testid="draft-confirm-continue" className="button-confirm-continue" icon="arrow" disabled={!checked} onClick={() => { setLeft(SEND_HOLD_SECONDS); setStep(2); }}>Continue</Button>
        </div>
      </> : <>
        <p className="send-confirm-warning" data-testid="draft-confirm-warning"><Icon name="alert" size={16} />This creates a real draft in PayPal Sandbox.</p>
        <p className="send-confirm-countdown" aria-live="polite" data-testid="draft-confirm-countdown">{left > 0 ? `Create is available in ${left} second${left === 1 ? '' : 's'}.` : 'You can create it now.'}</p>
        <div className="send-confirm-actions">
          <Button data-testid="draft-confirm-back" tone="ghost" onClick={onCancel}>Back</Button>
          <Button data-testid="draft-confirm-create" className={`button-confirm-send${left > 0 ? ' is-holding' : ''}`} icon="file" disabled={left > 0 || creating} loading={creating} onClick={create}>Create draft{left > 0 ? ` (${left})` : ''}</Button>
        </div>
      </>}
    </div>
  </div>, document.body);
}

// (foolproofing 2026-11-04) Reset demo empties the session (inputs, guide answers, drafts, the local review), so it
// asks once. The Sandbox connection stays.
function ResetConfirmDialog({ onCancel, onReset }) {
  const boxRef = useRef(null);
  const keyDown = useDialogFocus(boxRef, onCancel);
  return <div className="send-confirm-backdrop" data-testid="reset-confirm-backdrop">
    <div className="send-confirm" ref={boxRef} role="dialog" aria-modal="true" aria-labelledby="reset-confirm-title" data-testid="reset-confirm" onKeyDown={keyDown}>
      <h3 id="reset-confirm-title">Reset the demo?</h3>
      <p data-testid="reset-confirm-text">This clears this session's checks, sales, dispute cases, evidence drafts and the local review. Your text and the Sandbox connection stay. A draft already in PayPal Sandbox is not deleted.</p>
      <div className="send-confirm-actions">
        <Button data-testid="reset-confirm-cancel" tone="ghost" onClick={onCancel}>Back</Button>
        <Button data-testid="reset-confirm-reset" className="button-confirm-continue" icon="refresh" onClick={onReset}>Reset demo</Button>
      </div>
    </div>
  </div>;
}

// (evloop) Under a failed provide-evidence, tracking or invoice send: PayPal's own reason in plain English, from the
// sanitised codes the backend kept (never PayPal's free text), with the PayPal-Debug-Id for PayPal support.
function PaypalIssueNote({ error }) {
  const lines = paypalIssueLines(error?.paypalIssue);
  if (!lines.length && !error?.paypalDebugId) return null;
  return <span className="paypal-issue" data-testid="paypal-issue">
    {lines.map((line) => <span key={line} className="paypal-issue-line" data-testid="paypal-issue-line"> {line}</span>)}
    {error.paypalDebugId && <span className="paypal-issue-debug" data-testid="paypal-issue-debug"> PayPal debug ID {error.paypalDebugId}.</span>}
  </span>;
}

// (optimise r24) Next to "Confirm local draft review": the provide-evidence request exactly as the server would send
// it (method, path, evidence types, masked tracking rows, file parts), open by default, plus the payload sha256 when
// the preview response carries one ("—" otherwise).
function ApprovalPayloadCard({ preview, caseRef, hosted = false }) {
  const current = preview && preview.case_ref === caseRef ? preview : null;
  return <details className="approval-payload" data-testid="approval-payload" open>
    <summary><Icon name="file" size={16} /><span>Request PayPal would receive</span></summary>
    {current ? <dl className="approval-payload-list">
      <div><dt>Request</dt><dd data-testid="approval-payload-request">{current.method} {current.path}</dd></div>
      <div><dt>Evidence types</dt><dd data-testid="approval-payload-types">{current.input.evidences.map((row) => row.evidence_type).join(', ')}</dd></div>
      <div><dt>Tracking (masked)</dt><dd data-testid="approval-payload-tracking">{current.input.evidences.flatMap((row) => row.evidence_info.tracking_info).map((row) => `${row.carrier_name === 'OTHER' ? row.carrier_name_other : row.carrier_name} ${row.tracking_number}`).join('; ') || 'None'}</dd></div>
      <div><dt>File parts</dt><dd data-testid="approval-payload-files">{current.files.map((part) => `${part.name}: ${part.filename} (${part.content_type}, ${part.byte_length} bytes)`).join('; ') || 'None'}</dd></div>
      <div><dt title={FINGERPRINT_NOTE}>Request fingerprint (session-keyed SHA-256)</dt><dd data-testid="approval-payload-sha256" className="approval-payload-hash">{current.payload_sha256 || '—'}</dd></div>
      <div><dt>Status</dt><dd>{operatorLabel(current.external_send)} · {current.data_source_label} data · {current.content_type}</dd></div>
    </dl> : hosted ? <p className="text-dim" data-testid="approval-payload-empty">Hosted demo: no PayPal request is built here and nothing is sent.</p> : <p className="text-dim" data-testid="approval-payload-empty">Not prepared yet. Pick this case's dispute in the PayPal list below and prepare the preview.</p>}
  </details>;
}

// (optimise r24) Step 03 lists what came from step 01, so the three steps read as one flow.
function StepOneEvidence({ productConfirm, countryCheck, lostCheck = null }) {
  const product = productConfirm?.choice === 'CONFIRMED' ? `Confirmed product card: ${productConfirm.card.title}. Added to the review ZIP as product-reference.json.`
    : productConfirm ? 'Your answer that none of the catalogue products is yours. Added to the review ZIP as product-reference.json.'
    : 'No product card confirmed in step 01.';
  const country = countryCheck ? `Country check ${countryCheck.seller_country} → ${countryCheck.buyer_country}: ${countryCheck.blocked ? 'Stopped' : countryCheck.postal ? 'post will not carry it' : 'no cited rule stops it'} at ${new Date(countryCheck.at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hourCycle: 'h23' })}. Shown here for context; not in the review ZIP.`
    : lostCheck ? `Run the country check again in step 01: the ${lostCheck.seller_country} → ${lostCheck.buyer_country} result ended with the expired session.`
    : 'No country check run in step 01.';
  return <div className="step-one-evidence" data-testid="step-one-evidence"><span className="step-one-tag">From step 01</span>
    <ul><li data-testid="step-one-product">{product}</li><li data-testid="step-one-country">{country}</li></ul></div>;
}

function ScenarioMatchPanel({ match }) {
  const scenario = match?.scenario;
  if (!scenario) return null;
  return <details className="scenario-match" data-testid="dispute-scenario-match"><summary><Icon name="link" size={15} /><span>Bound synthetic scenario</span><Badge tone="muted">{scenario.citations.length} pinned citations</Badge></summary><div className="scenario-match-body"><div className="scenario-match-heading"><div><span className="meta-label">RULE-BASED CASE MATCH</span><strong>{scenario.title}</strong></div><Badge tone="amber">HUMAN REVIEW REQUIRED</Badge></div><ul>{scenario.citations.map((citation) => <li key={citation.chunk_id}><a href={citation.url} target="_blank" rel="noopener noreferrer">{citation.title}</a><span>{citation.locator}</span><code>{citation.chunk_id}</code></li>)}</ul><p>{operatorLabel(match.provenance)} · {operatorLabel(match.current_policy_applicability)} · {operatorLabel(match.operational_authority)}</p></div></details>;
}

function Metric({ label, value, unit, icon, detail, alert = false, compact = false, statusTone = 'neutral', testId }) {
  return <div data-testid={testId} className={`metric ${alert ? 'metric-alert' : ''} ${compact ? `metric-status metric-status-${statusTone}` : ''}`}><div className="metric-top"><span>{label}</span><Icon name={icon} /></div><div className={`metric-value ${compact ? 'metric-compact' : ''}`}><strong>{value}</strong>{unit && <span>{unit}</span>}</div><small>{detail}</small></div>;
}
