// Connect ("linked tags"): hover, focus or tap any element with data-link="<key>" inside a root and every element in
// that root with the same key is highlighted (.is-linked) and joined by a 1px right-angle line with 6px square ends,
// drawn in an SVG overlay (.tg-connect). The line turns risk-coloured (.tg-connect--risk) when any linked element
// carries data-link-risk. Plain DOM, no dependencies, no network. Spec: ui_mock/CONTAINER_SPEC.md; styles: components.css.

const SVG_NS = 'http://www.w3.org/2000/svg';
const END = 6; // px, square end marks

const GAP = 4; // px between a line end and the element's outline

// Length of the axis-aligned segment p->q that runs inside box r (0 when it misses).
function overlap(p, q, r) {
  const x1 = Math.max(Math.min(p.x, q.x), r.left); const x2 = Math.min(Math.max(p.x, q.x), r.left + r.width);
  const y1 = Math.max(Math.min(p.y, q.y), r.top); const y2 = Math.min(Math.max(p.y, q.y), r.top + r.height);
  if (x1 > x2 || y1 > y2) return 0;
  return Math.max(x2 - x1, y2 - y1, 0.5);
}

// Shortest right-angle path between neighbours a and b (boxes {left, top, width, height} relative to the root),
// starting and ending GAP px outside the midpoint of an edge. Overlapping rows give one horizontal line, overlapping
// columns one vertical line; otherwise an L with one turn: horizontal-then-vertical or vertical-then-horizontal,
// whichever runs the least distance through `obstacles` (other highlighted boxes); if both run through one, a two-turn
// route across the middle of the gap is used. Ties keep fewer turns, then the shorter line, then horizontal-first.
// Returns { d, start, end }.
export function elbowPath(a, b, obstacles = []) {
  const ac = { x: a.left + a.width / 2, y: a.top + a.height / 2 };
  const bc = { x: b.left + b.width / 2, y: b.top + b.height / 2 };
  const right = bc.x >= ac.x;
  const down = bc.y >= ac.y;
  const side = (box, toRight) => (toRight ? box.left + box.width + GAP : box.left - GAP);
  const edge = (box, toBottom) => (toBottom ? box.top + box.height + GAP : box.top - GAP);
  const rowsOverlap = a.top < b.top + b.height && b.top < a.top + a.height;
  const colsOverlap = a.left < b.left + b.width && b.left < a.left + a.width;
  const build = (pts) => ({ d: `M${pts[0].x} ${pts[0].y}` + pts.slice(1).map((p, k) => (p.x !== pts[k].x ? `H${p.x}` : `V${p.y}`)).join(''), start: pts[0], end: pts[pts.length - 1] });
  if (rowsOverlap && !colsOverlap) {
    const y = Math.round((Math.max(a.top, b.top) + Math.min(a.top + a.height, b.top + b.height)) / 2);
    return build([{ x: side(a, right), y }, { x: side(b, !right), y }]);
  }
  if (colsOverlap && !rowsOverlap) {
    const x = Math.round((Math.max(a.left, b.left) + Math.min(a.left + a.width, b.left + b.width)) / 2);
    return build([{ x, y: edge(a, down) }, { x, y: edge(b, !down) }]);
  }
  // Horizontal first: leave a's side, turn under / over b's centre, enter b's top or bottom.
  const hv = [{ x: side(a, right), y: ac.y }, { x: bc.x, y: ac.y }, { x: bc.x, y: edge(b, !down) }];
  // Vertical first: leave a's top or bottom, turn level with b's centre, enter b's side.
  const vh = [{ x: ac.x, y: edge(a, down) }, { x: ac.x, y: bc.y }, { x: side(b, !right), y: bc.y }];
  // Two-turn fallbacks for when both L shapes run through other boxes: out, across the gap's middle, in.
  const midY = Math.round((edge(a, down) + edge(b, !down)) / 2);
  const midX = Math.round((side(a, right) + side(b, !right)) / 2);
  const vhv = [{ x: ac.x, y: edge(a, down) }, { x: ac.x, y: midY }, { x: bc.x, y: midY }, { x: bc.x, y: edge(b, !down) }];
  const hvh = [{ x: side(a, right), y: ac.y }, { x: midX, y: ac.y }, { x: midX, y: bc.y }, { x: side(b, !right), y: bc.y }];
  const score = (pts) => {
    let hit = 0; let len = 0;
    for (let k = 1; k < pts.length; k += 1) {
      len += Math.abs(pts[k].x - pts[k - 1].x) + Math.abs(pts[k].y - pts[k - 1].y);
      for (const r of obstacles) hit += overlap(pts[k - 1], pts[k], r);
    }
    return [hit, pts.length, len];
  };
  const better = (x, y) => { const [p, q] = [score(x), score(y)]; return p[0] !== q[0] ? p[0] < q[0] : p[1] !== q[1] ? p[1] < q[1] : p[2] <= q[2]; };
  return build([vh, vhv, hvh].reduce((best, pts) => (better(pts, best) ? pts : best), hv));
}

// Length of a right-angle path made of M/H/V commands (for callers that animate or measure a line).
export function pathLength(d) {
  let x = 0;
  let y = 0;
  let total = 0;
  for (const [, cmd, raw] of String(d).matchAll(/([MHV])([^MHV]+)/g)) {
    const nums = raw.trim().split(/\s+/).map(Number);
    if (cmd === 'M') { [x, y] = nums; } else if (cmd === 'H') { total += Math.abs(nums[0] - x); [x] = nums; } else { total += Math.abs(nums[0] - y); [y] = nums; }
  }
  return total;
}

const reducedMotion = (win) => {
  try { return Boolean(win && win.matchMedia && win.matchMedia('(prefers-reduced-motion: reduce)').matches); } catch { return false; }
};

// Wire up one root (a container element). Returns a function that removes every listener and the overlay.
export function initConnect(root, { win = typeof window === 'undefined' ? null : window } = {}) {
  if (!root || typeof root.querySelectorAll !== 'function' || !win) return () => {};
  const doc = root.ownerDocument;
  if (win.getComputedStyle && win.getComputedStyle(root).position === 'static') root.style.position = 'relative';

  const svg = doc.createElementNS(SVG_NS, 'svg');
  svg.setAttribute('class', 'tg-connect');
  svg.setAttribute('aria-hidden', 'true');
  root.appendChild(svg);

  let activeKey = null;
  let pinned = false;
  const members = (key) => [...root.querySelectorAll('[data-link]')].filter((el) => el.dataset.link === key);
  const boxOf = (el, origin) => {
    const r = el.getBoundingClientRect();
    return { left: r.left - origin.left, top: r.top - origin.top, width: r.width, height: r.height };
  };

  const clear = () => {
    root.querySelectorAll('.is-linked').forEach((el) => el.classList.remove('is-linked'));
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    svg.setAttribute('class', 'tg-connect');
  };

  const draw = () => {
    clear();
    if (!activeKey) return;
    const els = members(activeKey);
    els.forEach((el) => el.classList.add('is-linked'));
    if (els.length < 2) return;
    const origin = root.getBoundingClientRect();
    const risk = els.some((el) => el.hasAttribute('data-link-risk'));
    const animate = !reducedMotion(win);
    svg.setAttribute('class', `tg-connect${risk ? ' tg-connect--risk' : ''}${animate ? ' is-drawing' : ''}`);
    // A linked element that contains another linked element (a clipping holding its source link) is highlighted but
    // not a line stop; it stays an obstacle. Neighbours only, in document order: A->B, B->C, C->D.
    const stops = els.filter((el) => !els.some((other) => other !== el && el.contains(other)));
    const all = els.map((el) => boxOf(el, origin));
    const boxes = stops.map((el) => all[els.indexOf(el)]);
    for (let i = 0; i < stops.length - 1; i += 1) {
      const { d, start, end } = elbowPath(boxes[i], boxes[i + 1], all.filter((b) => b !== boxes[i] && b !== boxes[i + 1]));
      const path = doc.createElementNS(SVG_NS, 'path');
      path.setAttribute('d', d);
      svg.appendChild(path);
      for (const p of [start, end]) {
        const rect = doc.createElementNS(SVG_NS, 'rect');
        rect.setAttribute('x', String(p.x - END / 2));
        rect.setAttribute('y', String(p.y - END / 2));
        rect.setAttribute('width', String(END));
        rect.setAttribute('height', String(END));
        svg.appendChild(rect);
      }
    }
  };

  const keyOf = (target) => {
    const el = target && target.closest ? target.closest('[data-link]') : null;
    return el && root.contains(el) ? el.dataset.link : null;
  };
  const show = (key) => { if (key !== activeKey) { activeKey = key; draw(); } };
  const onOver = (event) => { if (!pinned) { const key = keyOf(event.target); if (key) show(key); } };
  const onOut = (event) => {
    if (pinned) return;
    const next = keyOf(event.relatedTarget);
    if (next !== activeKey) show(next);
  };
  const onFocusIn = (event) => { const key = keyOf(event.target); if (key) { pinned = false; show(key); } };
  const onFocusOut = (event) => { if (!root.contains(event.relatedTarget)) { pinned = false; show(null); } };
  // Touch and click: tapping a linked element pins its key; tapping it again (or elsewhere in the root) clears it.
  const onClick = (event) => {
    const key = keyOf(event.target);
    if (key && !(pinned && key === activeKey)) { pinned = true; show(key); } else { pinned = false; show(null); }
  };
  const onKey = (event) => { if (event.key === 'Escape') { pinned = false; show(null); } };
  let frame = 0;
  const onResize = () => {
    if (!activeKey) return;
    if (frame) win.cancelAnimationFrame(frame);
    frame = win.requestAnimationFrame(() => { frame = 0; draw(); });
  };

  root.addEventListener('mouseover', onOver);
  root.addEventListener('mouseout', onOut);
  root.addEventListener('focusin', onFocusIn);
  root.addEventListener('focusout', onFocusOut);
  root.addEventListener('click', onClick);
  root.addEventListener('keydown', onKey);
  win.addEventListener('resize', onResize);
  const observer = typeof win.ResizeObserver === 'function' ? new win.ResizeObserver(onResize) : null;
  if (observer) observer.observe(root);

  return () => {
    root.removeEventListener('mouseover', onOver);
    root.removeEventListener('mouseout', onOut);
    root.removeEventListener('focusin', onFocusIn);
    root.removeEventListener('focusout', onFocusOut);
    root.removeEventListener('click', onClick);
    root.removeEventListener('keydown', onKey);
    win.removeEventListener('resize', onResize);
    if (observer) observer.disconnect();
    if (frame) win.cancelAnimationFrame(frame);
    clear();
    svg.remove();
  };
}
