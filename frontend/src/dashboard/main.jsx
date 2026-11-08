// AG Studio dispute evidence readiness dashboard (/dashboard.html), linked from the console and the evidence page.
// Synthetic data from files in the repository; no dispute decision. Studio's built-in agents use Gemini only
// when the local console has a model configured (governed backend route); the hosted demo replays a recorded
// run if one exists and otherwise says the agents are off.
import { useEffect, useMemo, useRef, useState, useSyncExternalStore } from 'react';
import { createRoot } from 'react-dom/client';
import { AgStudioAiModule, createAiHarness, directLlmRunner } from 'ag-studio';
import { AgStudio, AgStudioProvider, createWidgets } from 'ag-studio-react';
import disputesFile from '../data/dashboard_disputes_v1.json';
import benchmark from '../data/guide_benchmark_v1.json';
import receipts from '../data/channel3_receipts_v1.json';
import { rebaseDisputes, studioData } from './dashboardData.js';
import { PUBLIC_DEMO } from '../shared/asOfSource.js';
import { resolveAsOf } from '../shared/asOf.js';
import { initialReport, PAGE_TITLES, pageTracks } from './layout.js';
import { compactTheme, payguardTheme } from './theme.js';
import DelegateConfirm, { answerYes } from './DelegateConfirm.jsx';
import { CUSTOM_WIDGETS } from './widgets.jsx';
import { AUDITOR_ID, BOUNDARY, BUILT_IN_AGENT_IDS, createEvidenceAuditor, plainSummary, promptStarters } from './auditor.js';
import { createGeminiAdapter, createSessionClient, fetchAgentStatus } from './studioAgentClient.js';
import { createRecorder, recordingLabel, validateRecording } from './agentRecording.js';
import './dashboard.css';

// Read at build time only. Never commit a key: without one Studio runs as a trial with a watermark.
const LICENSE_KEY = typeof import.meta.env.VITE_AG_STUDIO_LICENSE === 'string' && import.meta.env.VITE_AG_STUDIO_LICENSE.trim()
  ? import.meta.env.VITE_AG_STUDIO_LICENSE.trim() : undefined;
const COMPACT_BREAKPOINT = 720;
// Canvas row height as rendered (theme.js sets studioCanvasRowHeight to 16).
const ROW_PX = 16;

// Same clock as the console (r20 UX-1): the cases are moved to the page's load time, so case-ref-001 shows the due date
// the console and its deadline board show. ?asof= can pin a time only in a build made with
// VITE_PAYGUARD_PUBLIC_DEMO=1 (shared/asOf.js); no build in this repository sets it, the hosted one included.
const LOAD_TIME = new Date().toISOString();
const disputes = rebaseDisputes(disputesFile, PUBLIC_DEMO ? resolveAsOf({ fileAsOf: LOAD_TIME, search: window.location.search, publicDemo: true }) : LOAD_TIME);
const data = studioData({ disputes, benchmark, receipts });
const tables = Object.fromEntries(data.sources.map((source) => [source.id, source.data]));
// The recorded run is optional: until the owner records one (tools/record_studio_agent_run.mjs) there is no file.
const recordedFiles = import.meta.glob('../data/studio_agent_run_v1.json', { eager: true, import: 'default' });
const RECORDING = (() => {
  const doc = Object.values(recordedFiles)[0];
  if (!doc) return null;
  try { return validateRecording(doc); } catch { return null; }
})();
const RECORD_MODE = new URLSearchParams(window.location.search).get('record') === '1';
// Default menu: Studio's own widgets plus the two TradeGlot widgets. A custom menu would also narrow the
// widget types the add_widget tool accepts, which the auditor needs for its answer grid.
const widgets = createWidgets({ additionalTypes: CUSTOM_WIDGETS });

// Decide once, before Studio is created (it reads the harness once): live built-in agents only when the
// backend says a model is configured; otherwise a recorded run (hosted demo) or none.
async function bootstrap() {
  const client = createSessionClient();
  const status = await fetchAgentStatus(client);
  return { mode: status === 'live' ? 'live' : RECORDING ? 'replay' : 'off', client };
}

const STUDIO_MAX_TURNS = 8;

// (r32 J3) Before an answer, the auditor clears the seller's own selections on that page (the cross filter from a
// click and the values of page filters such as "Filter by case"), so its grid shows exactly the rows of the reply.
// The page filters themselves stay; only their values are reset.
function clearPageSelections(api, pageId) {
  const state = api.getState();
  api.setState({
    ...state,
    pages: state.pages.map((page) => (page.id !== pageId ? page : {
      ...page,
      crossFilter: undefined,
      ...(page.filter ? { filter: { ...page.filter, page: page.filter.page?.map(({ model, ...rest }) => rest) } } : {}),
    })),
  });
}

function makeHarness({ mode, client, onAnswer, onDelegated, onConfirmNeeded, recorder }) {
  return ({ api }) => createAiHarness(api, ({ tools, builtIn }) => {
    const live = mode === 'live';
    const adapter = live ? createGeminiAdapter(client) : null;
    const auditor = createEvidenceAuditor({
      studio: tools.studio, getState: () => api.getState(), data: tables, onAnswer, onDelegated, onConfirmNeeded, recorder,
      delegate: live ? tools.delegateTo(['data']) : null, recording: live ? null : RECORDING,
      clearSelections: (pageId) => clearPageSelections(api, pageId),
    });
    return {
      // (red team r27 A) A hard turn cap behind the adapter's forced finish at turn five.
      agents: [auditor, ...(live ? BUILT_IN_AGENT_IDS.map((id) => directLlmRunner({ ...builtIn[id], adapter, maxTurns: STUDIO_MAX_TURNS })) : [])],
      primary: AUDITOR_ID,
      promptStarters: promptStarters({ mode, recording: RECORDING }),
      observers: recorder ? [recorder.observer] : [],
    };
  });
}

const AGENT_STATUS = {
  live: "on: they use Gemini through the console's governed route (local live mode). The auditor hands questions outside its own set to Studio's data agent.",
  replay: RECORDING ? `replayed: ${recordingLabel(RECORDING)}` : '',
  off: 'off: no model is configured, and the hosted demo makes no model calls.',
};

// Phone or desktop layout is chosen at load (plan r2 F22). Studio is no longer remounted on a size change (red team
// r27 B: that dropped the AI thread mid-answer); the new layout applies on the next load.
// AG Studio names its widget toolbar buttons with raw locale keys (aria-label "widgetToolbarDelete" and so on). This
// page is read only: duplicate and delete are hidden, and export or download buttons get readable names
// (click-all 2026-11-03 #13).
const TOOLBAR_LABELS = {
  gridWidgetFormSectionExport: 'Export table', chartWidgetFormSectionExport: 'Export chart',
  chartWidgetFormSectionDownload: 'Download chart',
};
const TOOLBAR_HIDDEN = ['widgetToolbarDuplicate', 'widgetToolbarDelete'];
// Every attribute set here is set only when it differs, so the MutationObserver that calls this settles.
const setAttr = (el, name, value) => { if (el.getAttribute(name) !== value) el.setAttribute(name, value); };
function fixToolbarButtons(root) {
  for (const button of root.querySelectorAll('.ag-studio-widget-toolbar-button[aria-label]')) {
    const key = button.getAttribute('aria-label');
    if (TOOLBAR_HIDDEN.includes(key)) { button.hidden = true; setAttr(button, 'aria-hidden', 'true'); setAttr(button, 'tabindex', '-1'); }
    else if (TOOLBAR_LABELS[key]) { setAttr(button, 'aria-label', TOOLBAR_LABELS[key]); button.title = TOOLBAR_LABELS[key]; }
  }
  // Each widget's Tab stop was an empty 0x0 focus container (Studio's widget tab guards send focus there): ten
  // nameless, invisible stops before the AI panel, and in edit mode Tab could not get past one (attack r22). The
  // widget guards and containers leave the Tab order, so Tab walks the widgets' real controls (grids keep their own
  // guards). Each container is named after its widget, because focusAnswer focuses it by script.
  for (const guard of root.querySelectorAll('.ag-studio-layout-widget > .ag-tab-guard')) setAttr(guard, 'tabindex', '-1');
  for (const stop of root.querySelectorAll('.ag-studio-layout-widget-focus-container')) {
    setAttr(stop, 'tabindex', '-1');
    const title = stop.closest('.ag-studio-layout-widget')?.querySelector('.ag-studio-layout-widget-title')?.textContent?.trim();
    if (title) { setAttr(stop, 'role', 'group'); setAttr(stop, 'aria-label', `${title} widget`); }
  }
  // Chrome makes a scrollable element a Tab stop when it has no tabindex. AG Grid's own Tab handling then sends focus
  // from the last cell to its scroll viewport and back again, so Tab never left the Cases grid (attack r22). The grid
  // keeps its cells and arrow keys; the scroll viewports leave the Tab order.
  for (const scroller of root.querySelectorAll('.ag-body-vertical-scroll-viewport, .ag-body-horizontal-scroll-viewport')) setAttr(scroller, 'tabindex', '-1');
  // Widget-type icons in edit mode are decorative svgs next to the widget title (attack r22: 8 unnamed images).
  for (const svg of root.querySelectorAll('.ag-studio-widget-icon-container svg')) { setAttr(svg, 'aria-hidden', 'true'); setAttr(svg, 'focusable', 'false'); }
}

// The next (or previous) Tab stop in the document outside `container`, for leaving a grid (attack r22).
const TABBABLE = 'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), summary, [tabindex]';
function tabStopOutside(container, backwards) {
  const stops = [...document.querySelectorAll(TABBABLE)].filter((el) => el.tabIndex >= 0 && !el.hidden && !el.contains(container)
    && !el.closest('[inert], [aria-hidden="true"]') && (el.getClientRects().length > 0 || el.classList.contains('ag-tab-guard')));
  if (backwards) {
    const before = stops.filter((el) => !container.contains(el) && (container.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_PRECEDING));
    return before[before.length - 1] || null;
  }
  return stops.find((el) => !container.contains(el) && (container.compareDocumentPosition(el) & Node.DOCUMENT_POSITION_FOLLOWING)) || null;
}

// The answer grid the auditor builds (auditor.js titles it "Evidence auditor · ..."); Studio puts no widget id in the DOM.
const ANSWER_TITLE_PREFIX = 'Evidence auditor ·';
function findAnswerWidget(root) {
  for (const widget of root?.querySelectorAll('.ag-studio-layout-widget') || []) {
    const title = widget.querySelector('.ag-studio-layout-widget-title')?.textContent || '';
    if (title.startsWith(ANSWER_TITLE_PREFIX) && widget.getClientRects().length > 0) return widget;
  }
  return null;
}

// Compact (phone) layout: a narrow screen, a short one (a phone held sideways is about 720x266 CSS px) or a touch
// screen. Width alone missed phones in landscape, where opening the auditor focused the message box and the
// floating keyboard covered the page (attack r23).
const SHORT_BREAKPOINT = 480;
// Layout follows size only, so a touch tablet keeps the wide layout; touch alone decides where focus goes (touchQuery).
const compactQuery = window.matchMedia(`(max-width: ${COMPACT_BREAKPOINT}px), (max-height: ${SHORT_BREAKPOINT}px)`);
const subscribeCompact = (notify) => { compactQuery.addEventListener('change', notify); return () => compactQuery.removeEventListener('change', notify); };
// Where focus goes in the AI panel. On a touch screen (or any compact one) focusing the message box pops up the
// keyboard over the panel, so the panel heading takes focus there; elsewhere the message box (attack r23).
const touchQuery = window.matchMedia('(pointer: coarse), (hover: none)');
const panelFocusTarget = (root) => (compactQuery.matches || touchQuery.matches
  ? root?.querySelector('.ag-studio-panel-header')
  : root?.querySelector('.ag-studio-ai-assistant-textarea'));
// The panel sits below the intro and the drawer: at 1280x800 the message box had its top at 887 px, off screen, and
// focus({ preventScroll: true }) left the page where it was (attack r23). The Studio area is scrolled to just under
// the top bar (sticky except on short screens), which shows the whole panel because edit mode makes it one screen tall.
function scrollStudioIntoView(studio) {
  if (!studio) return;
  const topbar = document.querySelector('.pg-topbar');
  const offset = topbar && window.getComputedStyle(topbar).position === 'sticky' ? topbar.getBoundingClientRect().height : 0;
  const top = window.scrollY + studio.getBoundingClientRect().top - offset;
  const smooth = !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  window.scrollTo({ top: Math.max(0, top), behavior: smooth ? 'smooth' : 'auto' });
}

// (r33 M3) The starter answer was left above the viewport on a phone (scrollY 712, J4 r32): the smooth scroll ran
// while the panel was closing and the page below it still moved (Back restores the old scroll position, Studio
// lays the canvas out again). The answer is scrolled to just under the sticky top bar now and again once the layout
// has settled, the second time only if its top is still outside the screen.
function scrollAnswerIntoView(widget) {
  const go = (behavior) => {
    if (!widget.isConnected) return;
    const topbar = document.querySelector('.pg-topbar');
    const offset = topbar && window.getComputedStyle(topbar).position === 'sticky' ? topbar.getBoundingClientRect().height : 0;
    window.scrollTo({ top: Math.max(0, window.scrollY + widget.getBoundingClientRect().top - offset - 8), behavior });
  };
  const smooth = !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  go(smooth ? 'smooth' : 'auto');
  setTimeout(() => {
    const top = widget.getBoundingClientRect().top;
    if (top < 0 || top > window.innerHeight * 0.5) go('auto');
  }, 700);
}

function Dashboard({ setup }) {
  const compact = useSyncExternalStore(subscribeCompact, () => compactQuery.matches);
  const report = useMemo(() => initialReport({ compact }), [compact]);
  const apiRef = useRef(null);
  const [pageId, setPageId] = useState(report.selectedPageId);
  // A reload (pull-to-refresh) keeps the history entry of an open auditor panel. The page then opens the panel again,
  // so that entry and the screen agree and the next Back closes the panel instead of doing nothing (attack r22).
  const [mode, setMode] = useState(() => (window.history.state?.pgAuditor ? 'edit' : 'view'));
  const showPage = (id) => {
    const api = apiRef.current;
    if (!api || api.getState().selectedPageId === id) return;
    api.setState({ ...api.getState(), selectedPageId: id });
  };
  // Record mode (local live only): tools/record_studio_agent_run.mjs drives the page and reads the recording.
  const recorder = useMemo(() => (RECORD_MODE && setup.mode === 'live' ? createRecorder({ getState: () => apiRef.current?.getState() }) : null), [setup.mode]);
  useEffect(() => {
    if (recorder) window.__payguardRecorder = { finish: (options) => recorder.finish(options) };
  }, [recorder]);
  const studioRef = useRef(null);
  useEffect(() => {
    const root = studioRef.current;
    if (!root) return undefined;
    fixToolbarButtons(root);
    const observer = new MutationObserver(() => fixToolbarButtons(root));
    observer.observe(root, { childList: true, subtree: true, attributes: true, attributeFilter: ['aria-label', 'tabindex', 'aria-hidden', 'role'] });
    // Studio hides the question chips with aria-hidden as soon as one is used, while the tapped chip still has focus
    // (browser warning "Blocked aria-hidden ... retained focus", attack r22). In the capture phase, before Studio's own
    // click handler, focus moves to the panel: the message box on a wide screen, the panel heading on a phone (no
    // keyboard pops up there; the answer is focused next anyway).
    const onChip = (event) => {
      if (!event.target.closest?.('.ag-studio-ai-prompt-starter')) return;
      panelFocusTarget(root)?.focus({ preventScroll: true }); // touch: heading, no keyboard (attack r23)
    };
    root.addEventListener('click', onChip, true);
    // In edit mode Tab went from the last Cases cell to the grid's scroll viewport and back for ever (attack r22).
    // A grid is one Tab stop here: arrow keys move between cells, Tab and Shift+Tab leave the widget that holds it.
    const onGridTab = (event) => {
      if (event.key !== 'Tab' || event.altKey || event.ctrlKey || event.metaKey) return;
      const cell = event.target.closest?.('.ag-root-wrapper [role="gridcell"], .ag-root-wrapper [role="columnheader"]');
      if (!cell) return;
      const target = tabStopOutside(cell.closest('.ag-studio-layout-widget') || cell.closest('.ag-root-wrapper'), event.shiftKey);
      if (!target) return;
      event.preventDefault();
      event.stopPropagation();
      target.focus();
    };
    root.addEventListener('keydown', onGridTab, true);
    return () => { observer.disconnect(); root.removeEventListener('click', onChip, true); root.removeEventListener('keydown', onGridTab, true); };
  }, []);
  const theme = useMemo(() => (compact ? compactTheme(window.innerWidth) : payguardTheme), [compact]);
  const modeButtonRef = useRef(null);
  // Studio hides the AI panel with aria-hidden when the mode goes back to view. If focus is still inside it (a
  // question chip), the browser warns and drops focus to BODY, so focus moves to the mode button first (attack r21).
  const focusOutOfPanel = () => {
    const active = document.activeElement;
    if (active && active !== document.body && studioRef.current?.contains(active)) modeButtonRef.current?.focus({ preventScroll: true });
  };
  // The open auditor panel is a history entry, so the phone's Back button closes it instead of leaving the page
  // (attack r21). Closing it any other way consumes that entry.
  // history.back() is asynchronous: until its popstate arrives the entry still says pgAuditor, so a fast second or
  // third tap called back() again and left the page (attack r22). One back per open; taps wait for the popstate.
  const backPendingRef = useRef(false);
  const openAuditor = () => {
    if (backPendingRef.current) return;
    if (!window.history.state?.pgAuditor) window.history.pushState({ ...(window.history.state || {}), pgAuditor: true }, '');
    focusPanelRef.current = true;
    setMode('edit');
  };
  const closeAuditor = () => {
    if (backPendingRef.current) return;
    focusOutOfPanel();
    if (window.history.state?.pgAuditor) {
      backPendingRef.current = true;
      window.history.back(); // the popstate handler sets view mode
    } else setMode('view');
  };
  const toggleAuditor = () => (mode === 'view' ? openAuditor() : closeAuditor());
  useEffect(() => {
    const onPop = (event) => {
      backPendingRef.current = false;
      if (event.state?.pgAuditor) { setMode('edit'); return; }
      focusOutOfPanel();
      setMode('view');
    };
    const onShow = () => { backPendingRef.current = false; };
    window.addEventListener('popstate', onPop);
    window.addEventListener('pageshow', onShow);
    return () => { window.removeEventListener('popstate', onPop); window.removeEventListener('pageshow', onShow); };
  }, []); // eslint-disable-line react-hooks/exhaustive-deps
  // Opening the auditor moved no focus: it stayed on the toggle, 19 Tabs from the message box (attack r22). Once
  // Studio has drawn the panel, focus goes into it: the message box on a wide screen, the panel heading on a phone,
  // where focusing the box would pop the keyboard over the panel.
  const focusPanelRef = useRef(false);
  useEffect(() => {
    if (mode !== 'edit' || !focusPanelRef.current) return undefined;
    focusPanelRef.current = false;
    let timer = 0;
    const tryFocus = (triesLeft) => {
      const root = studioRef.current;
      const target = panelFocusTarget(root);
      if (target && target.getClientRects().length > 0) {
        target.focus({ preventScroll: true });
        scrollStudioIntoView(root); // the panel was focused off screen (attack r23)
      } else if (triesLeft > 0) timer = setTimeout(() => tryFocus(triesLeft - 1), 100);
    };
    tryFocus(20);
    return () => clearTimeout(timer);
  }, [mode]);
  // After an answer on a phone, focus the new answer grid (its focus container is Studio's own tab stop) and
  // bring it into view; until Studio has drawn it, the canvas is scrolled to instead (attack r21).
  const focusAnswer = (triesLeft = 10) => {
    const widget = findAnswerWidget(studioRef.current);
    const target = widget?.querySelector('.ag-studio-layout-widget-focus-container[tabindex]') || null;
    if (target) {
      target.focus({ preventScroll: true });
      scrollAnswerIntoView(widget);
    } else if (triesLeft > 0) setTimeout(() => focusAnswer(triesLeft - 1), 150);
    else studioRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };
  // When the auditor answers on the other page, show that page. On a phone the AI panel covers the canvas, so
  // the dashboard goes back to view mode and moves to the answer slot under the headline tiles. The breakpoint is
  // read when the answer comes, not when the harness was made.
  const onAnswer = (page, technical) => {
    const phone = compactQuery.matches;
    if (technical) setTechnical(technical);
    setTimeout(() => {
      showPage(page);
      if (phone) {
        closeAuditor();
        setTimeout(() => focusAnswer(), 300);
      }
    }, phone ? 900 : 0);
  };
  // (red team r27 B) The data agent's last answer, shown above the canvas so a Studio remount cannot hide it.
  const [delegated, setDelegated] = useState(null);
  // (r31 J1 J4) The exact Studio tool steps of the auditor's last answer; the reply itself says them in plain words.
  const [technical, setTechnical] = useState(null);
  const [confirmQuestion, setConfirmQuestion] = useState(null);
  const ai = useMemo(() => makeHarness({ ...setup, recorder, onAnswer, onDelegated: setDelegated, onConfirmNeeded: setConfirmQuestion }), [setup, recorder]); // eslint-disable-line react-hooks/exhaustive-deps
  const currentPage = report.pages.find((page) => page.id === pageId) || report.pages[0];
  // One scroll: in view mode Studio is exactly as tall as the current page; in edit mode it fills the screen under
  // the sticky top bar so the AI panel has room.
  const studioHeight = mode === 'edit' ? 'calc(100svh - 56px)' : `${pageTracks(currentPage) * ROW_PX + 60}px`;
  const asOf = `${disputes.as_of.slice(0, 16).replace('T', ' ')} UTC`;
  return (
    <div className="pg-dashboard">
      <DelegateConfirm question={confirmQuestion} onCancel={() => setConfirmQuestion(null)} onSend={() => { setConfirmQuestion(null); answerYes(); }} />
      <header className="pg-topbar">
        <p className="pg-brand">TradeGlot <span>· AG Studio</span> <a className="pg-back" href="/" data-testid="dashboard-back-to-console">Back to console</a></p>
        <nav className="pg-tabs" aria-label="Dashboard pages">
          {report.pages.map((page) => (
            <button key={page.id} type="button" aria-pressed={pageId === page.id} className={pageId === page.id ? 'is-active' : ''}
              data-testid={`dashboard-page-${page.id}`} onClick={() => showPage(page.id)}>{PAGE_TITLES[page.id]}</button>
          ))}
        </nav>
        <button type="button" className="pg-mode" data-testid="dashboard-mode" aria-pressed={mode === 'edit'} ref={modeButtonRef}
          onClick={toggleAuditor}>{mode === 'view' ? 'Ask the auditor' : 'Back to view'}</button>
      </header>
      <section className="pg-intro">
        {/* The heading follows the page tab (click-all 2026-11-03 #12). */}
        <h1 data-testid="dashboard-heading">{currentPage.id === 'readiness' ? 'Dispute evidence readiness' : PAGE_TITLES[currentPage.id]}</h1>
        <p>Demo cases, {asOf}. Read only: it decides nothing and submits nothing.</p>
        <ul className="pg-chips" aria-label="Status">
          <li>Auditor: on</li>
          <li className={setup.mode === 'off' ? '' : 'is-accent'}>Built-in agents: {setup.mode}</li>
          <li>Licence: {LICENSE_KEY ? 'key' : 'trial'}</li>
          {/* (r31 J1 J4) No "Changes stay in this tab" chip: the drawer below says it in edit mode ("Edit mode: ..."). */}
        </ul>
        {delegated && <p className="pg-delegated" role="status" aria-live="polite" data-testid="dashboard-delegated"><strong>Data agent:</strong> {plainSummary(delegated.summary)}</p>}
      </section>
      <details className="pg-drawer">
        <summary>About this data and its limits</summary>
        <div className="pg-drawer-body">
          <p className="pg-boundary">{BOUNDARY}</p>
          <ul className="pg-status" data-testid="dashboard-status">
            <li><strong>Evidence auditor:</strong> on. Seven questions answered with code and built with Studio tools. Open it with “Ask the auditor”.</li>
            <li data-testid="dashboard-built-in" data-mode={setup.mode}><strong>Built-in agents:</strong> {AGENT_STATUS[setup.mode]}</li>
            <li data-testid="dashboard-licence"><strong>Licence:</strong> {LICENSE_KEY ? 'AG Studio key supplied at build time (the hosted demo uses a trial or development key, not a purchased production licence).' : 'no key in this build: AG Studio runs as a trial, logs a licence notice and may show its watermark.'}</li>
            {mode === 'edit' && <li><strong>Edit mode:</strong> the auditor and layout changes stay in this tab and are not saved.</li>}
          </ul>
          {technical && <details className="pg-technical" data-testid="dashboard-technical-steps">
            <summary>Technical steps</summary>
            <ol>{technical.map((step) => <li key={step.tool}><code>{step.tool}</code>: {step.detail}</li>)}</ol>
          </details>}
          <p className="pg-sources">Sources: frontend/src/data/dashboard_disputes_v1.json (tools/build_dashboard_data.py), guide_benchmark_v1.json, channel3_receipts_v1.json; the recorded guide benchmark and the recorded Channel3 searches. Method and limits: docs/AG_STUDIO_NOTES.md.</p>
        </div>
      </details>
      <main className="pg-studio" data-testid="dashboard-studio" ref={studioRef} style={{ height: studioHeight }}>
        {/* (red team r27 B) No key: a key that flips with the layout remounted Studio and dropped the thread and the canvas. */}
        <AgStudioProvider licenseKey={LICENSE_KEY} modules={[AgStudioAiModule]}>
          <AgStudio
            style={{ height: '100%', width: '100%' }}
            theme={theme}
            loadThemeGoogleFonts={false}
            data={data}
            widgets={widgets}
            initialState={report}
            mode={mode}
            ai={ai}
            panels={compact ? { edit: { right: ['ai'] }, view: { right: [] } } : { edit: { right: ['ai', 'filters'] }, view: { right: [] } }}
            onApiReady={(event) => { apiRef.current = event.api; }}
            onStateUpdated={(event) => setPageId(event.state.selectedPageId)}
          />
        </AgStudioProvider>
      </main>
      <footer className="pg-footer">
        <a href="/">Merchant console</a> · <a href="/evidence.html">Evidence page</a> · <a href="/proof.html" data-testid="dashboard-footer-proof">Proof</a>
      </footer>
    </div>
  );
}

function Root() {
  const [setup, setSetup] = useState(null);
  useEffect(() => { bootstrap().then(setSetup, () => setSetup({ mode: RECORDING ? 'replay' : 'off', client: null })); }, []);
  if (!setup) return <div className="pg-loading" role="status">Loading the dashboard…</div>;
  return <Dashboard setup={setup} />;
}

createRoot(document.getElementById('root')).render(<Root />);
