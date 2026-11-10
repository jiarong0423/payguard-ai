// Deadline board cards stay readable with many cards (2026-11-10: on the hosted site, ten cards in a row of six crushed
// each value cell to 1-2 letters). Pins the CSS rules: a minimum card width, facts sized by the card itself (container
// query), label above value, no mid-word break, and no wide-screen file overriding the card or fact layout.
import assert from 'node:assert/strict';
import { readdirSync, readFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const css = readFileSync(join(root, 'frontend/src/board/board.css'), 'utf8').replace(/\/\*[\s\S]*?\*\//gu, '');
const rule = (selector) => {
  const match = css.match(new RegExp(`(?:^|\\n)${selector.replace(/[.*+?^${}()|[\]\\]/gu, '\\$&')} \\{([^}]*)\\}`, 'u'));
  assert.ok(match, `${selector} rule present`);
  return match[1];
};

// 1. (2026-11-10 redesign, red-team R1) Cards are one horizontal strip of fixed-width cards (330px, or most of a phone's
// width): the list never cuts a row of cards in half and never squeezes a card.
assert.match(css, /\.board-list \{ display: flex;[^}]*overflow-x: auto;/u, 'cards are one sideways strip');
const cardBasis = css.match(/\.board-list > \.board-row \{ flex: 0 0 clamp\((\d+)px, \d+%, \d+px\);/u);
assert.ok(cardBasis && Number(cardBasis[1]) >= 260, 'card width >= 260px, a part of the next card always shows');

// 2. Facts: the card is a size container; fact columns come from the card width, each at least 130px; label above value.
assert.match(rule('.board-row'), /container-type: inline-size/u);
const facts = rule('.board-row dl');
const factMin = facts.match(/repeat\(auto-fill, minmax\((\d+)px, 1fr\)\)/u);
assert.ok(factMin && Number(factMin[1]) >= 120, 'fact columns >= 120px each');
assert.match(rule('.board-row dl > div'), /display: block/u, 'label above value, not a squeezed label column');
assert.match(css, /@container \(max-width: \d+px\) \{\s*\.board-row dl \{ grid-template-columns: minmax\(0, 1fr\); \}/u, 'narrow card: one fact per line');

// 2b. (2026-11-10 redesign) Compact fixed-shape card: one line per fact, a fixed two-line plan area, and the list and
// the timeline each scroll inside their own box so the board is one tool on the page, not the whole page.
assert.match(rule('.board-list .board-row dl > div'), /white-space: nowrap;[^}]*text-overflow: ellipsis/u, 'one line per fact');
assert.match(rule('.board-list .board-row dl > div:nth-child(5)'), /height: \d+px/u, 'plan area has a fixed height in every state');
assert.match(css, /\.board-plan-message \{ flex: 1 1 0;[^}]*white-space: nowrap;/u, 'plan line keeps one height');
assert.match(css, /\.board-timeline:not\(\.board-timeline-phone\) \.board-canvas \.b-sch-event-wrap \{ height: \d+px !important; --b-event-size: \d+ !important; \}/u, 'desktop timeline bars share one lane height');
const boardJsx = readFileSync(join(root, 'frontend/src/board/EvidenceBoard.jsx'), 'utf8');
assert.ok(boardJsx.includes("eventLayout={phone ? 'stack' : 'none'}") && boardJsx.includes('VISIBLE_ROWS * ROW_HEIGHT + TIMELINE_HEADER'), 'uniform rows; timeline has a fixed height past VISIBLE_ROWS');

// 3. No mid-word break: values wrap at spaces (break-word only for a single over-long token), never "anywhere".
const value = rule('.board-row dd');
assert.match(value, /overflow-wrap: break-word/u);
assert.match(value, /word-break: normal/u);
assert.doesNotMatch(css, /overflow-wrap: anywhere|word-break: break-all/u, 'nothing in the board breaks words anywhere');

// 4. The wide-screen files no longer set the card width or the fact grid (they are loaded later with #disputes and won).
const wideDir = join(root, 'frontend/src/wide');
for (const name of readdirSync(wideDir).filter((file) => file.endsWith('.css'))) {
  const text = readFileSync(join(wideDir, name), 'utf8').replace(/\/\*[\s\S]*?\*\//gu, '');
  assert.doesNotMatch(text, /\.board-list \{[^}]*grid-template-columns/u, `${name}: no card width override`);
  assert.doesNotMatch(text, /\.board-row dl \{[^}]*grid-template-columns/u, `${name}: no fact column override`);
  assert.doesNotMatch(text, /\.board-row dl > div \{/u, `${name}: no label/value grid override`);
}

// 5. Timeline grid (2026-11-10, live df4799a): short grid text so no locked cell wraps past its row; two-line Case cell;
// readable plan bars; milestone labels short with the full name as a title.
const { gridEvidenceLabel, gridReasonLabel, GRID_TEXT_MAX } = await import('../frontend/src/board/boardData.js');
for (const status of ['WAITING_FOR_SELLER_RESPONSE', 'WAITING_FOR_BUYER_RESPONSE', 'UNDER_REVIEW']) {
  const text = gridEvidenceLabel({ source: 'sandbox', providerStatus: status, readinessLabel: 'PayPal: long status words here' });
  assert.ok(text.length <= GRID_TEXT_MAX, `${status} -> "${text}" fits one grid line`);
}
assert.equal(gridEvidenceLabel({ source: 'synthetic', readinessLabel: '1/1 present' }), '1/1 present');
assert.equal(gridReasonLabel('Item or service not received'), 'Not received');
const board = readFileSync(join(root, 'frontend/src/board/EvidenceBoard.jsx'), 'utf8');
assert.ok(Number(board.match(/const ROW_HEIGHT = (\d+);/u)[1]) >= 40, 'compact one-line rows (owner 2026-11-10: sized like the order table), two 18px lanes');
assert.ok(board.includes("field: 'gridEvidence'") && board.includes('class="board-grid-case"') && board.includes("escapeHtml(String(record.get('caseRef')"), 'Case cell: code then reason, escaped');
assert.ok(board.includes('<span class="ev-label" title="${full}">'), 'every bar label carries its full name as a title');
assert.ok(board.includes("CLAIM_OPENED: 'Claim'"), 'milestones use a short label');
assert.match(css, /\.board-canvas \.payguard-board-plan[^{]*\{ min-width: (\d+)px; \}/u, 'plan bars keep a visible width');
assert.match(css, /\.board-grid-case strong, \.board-grid-case small \{[^}]*text-overflow: ellipsis/u);

// 6. Wide screens: one content width for the top bar and the page; summaries have no caret-like chevron bar.
const scroll = readFileSync(join(root, 'frontend/src/wide/scroll.css'), 'utf8');
assert.match(scroll, /--pg-content-w: 1560px;/u);
assert.match(scroll, /\.topbar \{ padding-left: max\(24px, calc\(\(100vw - var\(--pg-content-w\)\) \/ 2\)\);/u);
assert.match(scroll, /\.main-content \{ width: min\(calc\(100% - 48px\), var\(--pg-content-w\)\);/u);
const index = readFileSync(join(root, 'frontend/src/index.css'), 'utf8');
assert.ok(index.includes('details:not(.limits-drawer) > summary::after { display: inline-block; }'), 'chevron is a box, not a lone border');

console.log(`frontend_board_card_layout: ok (cards >= ${cardBasis[1]}px, facts >= ${factMin[1]}px, no mid-word break)`);
