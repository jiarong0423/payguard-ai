// Connect ("linked tags"): hover, focus or tap any element with data-link="<key>" inside a root and every element in
// that root with the same key is highlighted (.is-linked) and joined by a 1px right-angle line with 6px square ends,
// drawn in an SVG overlay (.tg-connect). The line turns risk-coloured (.tg-connect--risk) when any linked element
// carries data-link-risk. Plain DOM, no dependencies, no network. Spec: ui_mock/CONTAINER_SPEC.md; styles: components.css.
// (F5 D-C1 2026-11-12) Lines only join members that are visible, inside the viewport and near each other, along a route
// that crosses no text; any member that cannot be reached that way is highlighted only. Hidden members are skipped.
// Escape (document), a click outside, hashchange, the root hiding, the pinned member scrolling out of view or leaving
// the DOM all clear the lines; scroll, resize and DOM changes redraw them from the current DOM.

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

const STEP = 6; // px between tried channels for two-turn routes
const PAD = 2; // px kept clear around text

// Intersection of two client rects (null when empty).
const intersect = (a, b) => {
  const left = Math.max(a.left, b.left); const top = Math.max(a.top, b.top);
  const right = Math.min(a.right, b.right); const bottom = Math.min(a.bottom, b.bottom);
  return right > left && bottom > top ? { left, top, right, bottom } : null;
};

// Shown at all: connected, not hidden by an attribute, CSS, a closed <details> or zero size. Highlight needs this.
function shown(el, win) {
  if (!el.isConnected || el.closest('[hidden]')) return false;
  if (typeof el.checkVisibility === 'function' && !el.checkVisibility({ checkOpacity: true, checkVisibilityCSS: true })) return false;
  for (let d = el.parentElement && el.parentElement.closest('details'); d; d = d.parentElement && d.parentElement.closest('details')) {
    if (!d.open) { const summary = d.querySelector(':scope > summary'); if (!summary || !summary.contains(el)) return false; }
  }
  const r = el.getBoundingClientRect();
  if (r.width < 1 || r.height < 1) return false;
  const cs = win.getComputedStyle ? win.getComputedStyle(el) : null;
  return !cs || (cs.visibility !== 'hidden' && cs.display !== 'none');
}

// The part of el actually on screen: clipped by every scrolling or clipping ancestor and by the viewport.
function onScreen(el, win) {
  const r = el.getBoundingClientRect();
  let box = intersect(r, { left: 0, top: 0, right: win.innerWidth, bottom: win.innerHeight });
  for (let p = el.parentElement; box && p && p !== el.ownerDocument.documentElement; p = p.parentElement) {
    const cs = win.getComputedStyle(p);
    if (/(auto|scroll|hidden|clip)/.test(cs.overflowX + cs.overflowY)) box = intersect(box, p.getBoundingClientRect());
  }
  return box && (box.right - box.left) * (box.bottom - box.top) >= 0.9 * r.width * r.height ? box : null;
}

// Every point of an axis-aligned route stays inside bounds and no segment or end mark touches an obstacle.
function clear(pts, obstacles, bounds) {
  for (const p of pts) if (p.x < bounds.left || p.x > bounds.right || p.y < bounds.top || p.y > bounds.bottom) return false;
  for (let k = 1; k < pts.length; k += 1) for (const r of obstacles) if (overlap(pts[k - 1], pts[k], r)) return false;
  for (const p of [pts[0], pts[pts.length - 1]]) {
    const mark = { left: p.x - END / 2, top: p.y - END / 2, width: END, height: END };
    for (const r of obstacles) if (mark.left < r.left + r.width && r.left < mark.left + END && mark.top < r.top + r.height && r.top < mark.top + END) return false;
  }
  return true;
}

// Shortest right-angle route between boxes a and b that crosses no obstacle (text), or null. Tries the straight and
// one-turn routes of elbowPath, then two-turn routes through every channel STEP px apart across the gap.
function clearRoute(a, b, obstacles, bounds) {
  const side = (box, toRight) => (toRight ? box.left + box.width + GAP : box.left - GAP);
  const edge = (box, toBottom) => (toBottom ? box.top + box.height + GAP : box.top - GAP);
  const ac = { x: a.left + a.width / 2, y: a.top + a.height / 2 };
  const bc = { x: b.left + b.width / 2, y: b.top + b.height / 2 };
  const right = bc.x >= ac.x; const down = bc.y >= ac.y;
  const cands = [];
  const rowsLo = Math.max(a.top, b.top) + 2; const rowsHi = Math.min(a.top + a.height, b.top + b.height) - 2;
  const colsLo = Math.max(a.left, b.left) + 2; const colsHi = Math.min(a.left + a.width, b.left + b.width) - 2;
  const colsOverlap = a.left < b.left + b.width && b.left < a.left + a.width;
  const rowsOverlap = a.top < b.top + b.height && b.top < a.top + a.height;
  if (rowsOverlap && !colsOverlap) for (let y = rowsLo; y <= rowsHi; y += STEP) cands.push([{ x: side(a, right), y: Math.round(y) }, { x: side(b, !right), y: Math.round(y) }]);
  if (colsOverlap && !rowsOverlap) for (let x = colsLo; x <= colsHi; x += STEP) cands.push([{ x: Math.round(x), y: edge(a, down) }, { x: Math.round(x), y: edge(b, !down) }]);
  if (!rowsOverlap && !colsOverlap) {
    cands.push([{ x: side(a, right), y: ac.y }, { x: bc.x, y: ac.y }, { x: bc.x, y: edge(b, !down) }]);
    cands.push([{ x: ac.x, y: edge(a, down) }, { x: ac.x, y: bc.y }, { x: side(b, !right), y: bc.y }]);
  }
  if (!rowsOverlap) {
    const y0 = edge(a, down); const y1 = edge(b, !down);
    for (let y = Math.min(y0, y1) + STEP; y < Math.max(y0, y1); y += STEP) {
      cands.push([{ x: ac.x, y: y0 }, { x: ac.x, y }, { x: bc.x, y }, { x: bc.x, y: y1 }]);
    }
  }
  if (!colsOverlap) {
    const x0 = side(a, right); const x1 = side(b, !right);
    for (let x = Math.min(x0, x1) + STEP; x < Math.max(x0, x1); x += STEP) {
      cands.push([{ x: x0, y: ac.y }, { x, y: ac.y }, { x, y: bc.y }, { x: x1, y: bc.y }]);
    }
  }
  const length = (pts) => pts.slice(1).reduce((sum, p, k) => sum + Math.abs(p.x - pts[k].x) + Math.abs(p.y - pts[k].y), 0);
  let best = null; let bestLen = Infinity;
  for (const pts of cands) {
    const fixed = pts.map((p) => ({ x: Math.round(p.x), y: Math.round(p.y) }));
    const len = length(fixed);
    if ((len < bestLen || (len === bestLen && fixed.length < best.length)) && clear(fixed, obstacles, bounds)) { best = fixed; bestLen = len; }
  }
  if (!best) return null;
  const pts = best.filter((p, k) => k === 0 || k === best.length - 1 || !(p.x === best[k - 1].x && p.y === best[k - 1].y));
  return { d: `M${pts[0].x} ${pts[0].y}` + pts.slice(1).map((p, k) => (p.x !== pts[k].x ? `H${p.x}` : `V${p.y}`)).join(''), start: pts[0], end: pts[pts.length - 1], len: bestLen };
}

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
  let source = null; // the member that was hovered, focused or tapped
  const members = (key) => [...root.querySelectorAll('[data-link]')].filter((el) => el.dataset.link === key && shown(el, win));

  const wipe = () => {
    root.querySelectorAll('.is-linked').forEach((el) => el.classList.remove('is-linked'));
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    svg.setAttribute('class', 'tg-connect');
  };

  // Text boxes (svg coordinates) inside `area`, each with the element that owns the text.
  const textBoxes = (origin, area) => {
    const out = [];
    const walker = doc.createTreeWalker(root, 4); // NodeFilter.SHOW_TEXT
    const range = doc.createRange();
    for (let node = walker.nextNode(); node; node = walker.nextNode()) {
      if (!node.nodeValue.trim() || svg.contains(node)) continue;
      const owner = node.parentElement;
      if (!owner || !intersect(owner.getBoundingClientRect(), area)) continue;
      range.selectNodeContents(node);
      for (const r of range.getClientRects()) {
        if (r.width > 0 && r.height > 0 && intersect(r, area)) out.push({ owner, left: r.left - origin.left - PAD, top: r.top - origin.top - PAD, width: r.width + 2 * PAD, height: r.height + 2 * PAD });
      }
    }
    // Controls, tags and other linked members count as whole boxes, so a line never runs along or through their border.
    for (const el of root.querySelectorAll('input:not([type=hidden]), textarea, select, img, button, a, .tg-tag, [data-link]')) {
      const r = el.getBoundingClientRect();
      if (r.width > 0 && intersect(r, area) && shown(el, win)) out.push({ owner: el, box: true, left: r.left - origin.left - PAD, top: r.top - origin.top - PAD, width: r.width + 2 * PAD, height: r.height + 2 * PAD });
    }
    return out;
  };

  const draw = () => {
    wipe();
    if (!activeKey) return;
    const rootBox = root.getBoundingClientRect();
    if (rootBox.width < 1 || rootBox.height < 1) { activeKey = null; pinned = false; source = null; return; }
    if (source && !source.isConnected) source = null;
    const els = members(activeKey);
    if (!els.length) { if (pinned) { activeKey = null; pinned = false; source = null; } return; }
    els.forEach((el) => el.classList.add('is-linked'));
    // The overlay is the coordinate system: every point is measured from it and must fall inside it.
    const origin = svg.getBoundingClientRect();
    const bounds = { left: 0, top: 0, right: origin.width, bottom: origin.height };
    // A linked element that contains another linked element (a clipping holding its source link, the case head holding
    // its case tag) is highlighted but not a line stop. Only members fully on screen are stops.
    const stops = els.filter((el) => !els.some((other) => other !== el && el.contains(other))).filter((el) => onScreen(el, win));
    if (stops.length < 2) return;
    const boxes = stops.map((el) => { const r = el.getBoundingClientRect(); return { left: r.left - origin.left, top: r.top - origin.top, width: r.width, height: r.height }; });
    const view = intersect(rootBox, { left: 0, top: 0, right: win.innerWidth, bottom: win.innerHeight });
    if (!view) return;
    const texts = textBoxes(origin, view);
    const limit = win.innerHeight; // no line longer than one viewport
    // Candidate pairs, nearest first; join a pair only when it links two groups not yet joined (a minimum spanning tree).
    const pairs = [];
    for (let i = 0; i < stops.length; i += 1) for (let j = i + 1; j < stops.length; j += 1) {
      const a = boxes[i]; const b = boxes[j];
      const dx = Math.max(0, a.left - (b.left + b.width), b.left - (a.left + a.width));
      const dy = Math.max(0, a.top - (b.top + b.height), b.top - (a.top + a.height));
      if (dx + dy <= limit) pairs.push({ i, j, gap: dx + dy });
    }
    pairs.sort((p, q) => p.gap - q.gap);
    const group = stops.map((_, k) => k);
    const find = (k) => (group[k] === k ? k : (group[k] = find(group[k])));
    const lines = [];
    for (const { i, j } of pairs) {
      if (find(i) === find(j)) continue;
      const a = boxes[i]; const b = boxes[j];
      const span = { left: Math.min(a.left, b.left) - END, top: Math.min(a.top, b.top) - END, right: Math.max(a.left + a.width, b.left + b.width) + END, bottom: Math.max(a.top + a.height, b.top + b.height) + END };
      const obstacles = texts.filter((t) => !stops[i].contains(t.owner) && !stops[j].contains(t.owner) && !(t.box && (t.owner.contains(stops[i]) || t.owner.contains(stops[j])))
        && t.left < span.right && span.left < t.left + t.width && t.top < span.bottom && span.top < t.top + t.height);
      const route = clearRoute(a, b, obstacles, bounds);
      if (!route || route.len > limit) continue;
      group[find(i)] = find(j);
      lines.push(route);
    }
    if (!lines.length) return;
    const risk = els.some((el) => el.hasAttribute('data-link-risk'));
    const animate = !reducedMotion(win);
    svg.setAttribute('class', `tg-connect${risk ? ' tg-connect--risk' : ''}${animate ? ' is-drawing' : ''}`);
    for (const { d, start, end } of lines) {
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

  const memberOf = (target) => {
    const el = target && target.closest ? target.closest('[data-link]') : null;
    return el && root.contains(el) ? el : null;
  };
  const show = (el) => {
    const key = el ? el.dataset.link : null;
    source = el;
    if (key !== activeKey) { activeKey = key; draw(); }
  };
  const reset = () => { pinned = false; source = null; if (activeKey) { activeKey = null; draw(); } };
  const onOver = (event) => { if (!pinned) { const el = memberOf(event.target); if (el) show(el); } };
  const onOut = (event) => {
    if (pinned) return;
    const next = memberOf(event.relatedTarget);
    if ((next ? next.dataset.link : null) !== activeKey) show(next);
  };
  const onLeave = () => { if (!pinned && !root.contains(doc.activeElement)) reset(); };
  const onFocusIn = (event) => { const el = memberOf(event.target); if (el) { pinned = false; show(el); } };
  const onFocusOut = (event) => { if (!root.contains(event.relatedTarget)) reset(); };
  // Touch and click: tapping a linked element pins its key; tapping it again, elsewhere in the root or outside it clears.
  const onClick = (event) => {
    const el = memberOf(event.target);
    if (el && !(pinned && el.dataset.link === activeKey)) { pinned = true; show(el); } else reset();
  };
  const onDocClick = (event) => { if (activeKey && !root.contains(event.target)) reset(); };
  const onKey = (event) => { if (event.key === 'Escape' && activeKey) reset(); };
  let frame = 0;
  const redraw = () => {
    if (!activeKey) return;
    if (frame) win.cancelAnimationFrame(frame);
    frame = win.requestAnimationFrame(() => {
      frame = 0;
      // A pinned member that left the DOM or scrolled out of view takes its lines with it.
      if (pinned && (!source || !source.isConnected || !shown(source, win) || !onScreen(source, win))) { reset(); return; }
      draw();
    });
  };
  const onResize = redraw;
  const onMutate = (records) => {
    if (records.some((m) => !svg.contains(m.target) && m.target !== svg)) redraw();
  };

  root.addEventListener('mouseover', onOver);
  root.addEventListener('mouseout', onOut);
  root.addEventListener('mouseleave', onLeave);
  root.addEventListener('focusin', onFocusIn);
  root.addEventListener('focusout', onFocusOut);
  root.addEventListener('click', onClick);
  doc.addEventListener('click', onDocClick, true);
  doc.addEventListener('keydown', onKey);
  doc.addEventListener('scroll', onResize, { capture: true, passive: true });
  win.addEventListener('hashchange', reset);
  win.addEventListener('resize', onResize);
  const observer = typeof win.ResizeObserver === 'function' ? new win.ResizeObserver(onResize) : null;
  if (observer) observer.observe(root);
  const mutations = typeof win.MutationObserver === 'function' ? new win.MutationObserver(onMutate) : null;
  if (mutations) mutations.observe(root, { childList: true, subtree: true, attributes: true, attributeFilter: ['hidden', 'open', 'data-link', 'style', 'aria-hidden'] });

  return () => {
    root.removeEventListener('mouseover', onOver);
    root.removeEventListener('mouseout', onOut);
    root.removeEventListener('mouseleave', onLeave);
    root.removeEventListener('focusin', onFocusIn);
    root.removeEventListener('focusout', onFocusOut);
    root.removeEventListener('click', onClick);
    doc.removeEventListener('click', onDocClick, true);
    doc.removeEventListener('keydown', onKey);
    doc.removeEventListener('scroll', onResize, { capture: true });
    win.removeEventListener('hashchange', reset);
    win.removeEventListener('resize', onResize);
    if (observer) observer.disconnect();
    if (mutations) mutations.disconnect();
    if (frame) win.cancelAnimationFrame(frame);
    wipe();
    svg.remove();
  };
}
