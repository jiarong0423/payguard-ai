// (P5 2026-11-12) Console Proof page: the ledger and the in-browser check show only values quoted from committed files.
//   1. The PDF copy in frontend/public/evidence has the SHA-256 and byte count recorded in READBACK_20261109.md.
//   2. Every {value, line} in proof_ledger_v1.json appears on that line of its evidence file.
//   3. The ledger's Debug-Ids are the ones overview_figures_v1.json lists for the same files and lines.
//   4. ProofPage.jsx types no number, hash, Debug-Id or date by hand, computes the hash with Web Crypto and fetches only
//      the same-origin PDF; ProofPage.css uses tokens only.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';

const read = (path) => readFileSync(new URL(`../${path}`, import.meta.url), 'utf8');
const ledger = JSON.parse(read('frontend/src/data/proof_ledger_v1.json'));
const figures = JSON.parse(read('frontend/src/data/overview_figures_v1.json'));
let checks = 0;
const ok = (value, message) => { assert.ok(value, message); checks += 1; };

// 1. The PDF.
const verify = ledger.verify;
const pdf = readFileSync(new URL(`../frontend/public/${verify.pdf}`, import.meta.url));
ok(createHash('sha256').update(pdf).digest('hex') === verify.recorded_sha256.value, 'PDF SHA-256 equals the recorded value');
ok(pdf.length === verify.byte_count, 'PDF byte count');
ok(verify.served_bytes.value === `${verify.byte_count.toLocaleString('en-US')} bytes`, 'served byte count matches the file');
ok(pdf.subarray(0, 5).toString('latin1') === '%PDF-', 'PDF header');
ok(verify.tamper_byte > 0 && verify.tamper_byte < pdf.length, 'tamper byte inside the file');
ok(ledger.sends.some((send) => send.id === verify.send_id && send.file === verify.file), 'verify row is a ledger row');

// 2. Quotes on their lines.
const quoteFields = ['date', 'where', 'debug_id', 'readback', 'file_check'];
const lineOf = (file, line) => read(file).split('\n')[line - 1] ?? '';
for (const send of ledger.sends) {
  ok(ledger.basis.some((item) => item.label === send.basis), `${send.id} basis in the legend`);
  for (const field of quoteFields) {
    const quote = send[field];
    if (!quote) continue;
    ok(lineOf(send.file, quote.line).includes(quote.value), `${send.id}.${field}: "${quote.value}" on ${send.file}:${quote.line}`);
  }
  if (send.file_check) ok(['match', 'not_compared'].includes(send.file_check.state), `${send.id} file_check state`);
}
for (const field of ['recorded_sha256', 'served_bytes']) {
  ok(lineOf(verify.file, verify[field].line).includes(verify[field].value), `verify.${field} on ${verify.file}:${verify[field].line}`);
}
ok(/SHA-256 recorded at send time/u.test(lineOf(verify.file, verify.recorded_sha256.line)), 'the cited line is the send-time fingerprint');
ok(new Set(ledger.basis.map((item) => item.label)).size === 4
  && ['RECORDED', 'RECOUNTED', 'SYNTHETIC', 'HOSTED DEMO'].every((label) => ledger.basis.some((item) => item.label === label)), 'four basis labels');

// 3. Same Debug-Ids as the Overview's send list (same file and line).
const overviewSends = [...figures.receipt_sends, ...figures.readback_sends];
ok(overviewSends.length === ledger.sends.length, 'one ledger row per send on the Overview');
for (const item of overviewSends) {
  const match = ledger.sends.find((send) => send.file === item.file && (item.debug_id ? send.debug_id?.value === item.debug_id : !send.debug_id));
  ok(match, `${item.file}:${item.line} (${item.debug_id}) has a ledger row`);
  if (item.debug_id) ok(match.debug_id.line >= item.line, `${item.debug_id} cited at or below the Overview's line (receipt line or section start)`);
}

// 4. Source hygiene.
const strip = (text) => text.replace(/\/\*[\s\S]*?\*\//gu, '').split('\n').filter((line) => !/^\s*(\/\/|import )/u.test(line)).join('\n');
const jsx = strip(read('frontend/src/pages/ProofPage.jsx'));
ok(!/\b[0-9a-f]{8,}\b/u.test(jsx), 'no hash or Debug-Id typed in ProofPage.jsx');
ok(!/\d{4}-\d{2}-\d{2}/u.test(jsx), 'no ISO date typed');
ok(!/\b\d{3,}\b|\d,\d{3}/u.test(jsx.replace(/SHA-256|shasum -a 256/gu, '')), 'no three-digit number typed (the algorithm name aside)');
for (const send of ledger.sends) for (const field of quoteFields) if (send[field]) ok(!jsx.includes(send[field].value) || send[field].value.length < 6, `${send.id}.${field} not typed`);
ok(jsx.includes("crypto.subtle.digest('SHA-256'"), 'hash computed with Web Crypto');
ok(/'MATCH'/u.test(jsx) && /'MISMATCH'/u.test(jsx), 'both verdicts rendered');
ok(/tg-stamp--ok/u.test(jsx) && /tg-stamp--risk/u.test(jsx), 'verdicts as stamps');
ok((jsx.match(/fetch\(/gu) || []).length === 1 && jsx.includes('fetch(`${import.meta.env.BASE_URL}${verify.pdf}`'), 'only the same-origin PDF is fetched');
ok(!/https?:\/\//u.test(jsx), 'no outside URL');
ok((jsx.match(/tg-btn--primary/gu) || []).length === 1, 'one primary button');
ok(/className="tg-ledger /u.test(jsx) && jsx.includes('tg-ledger__table') && jsx.includes('className="tg-log"'), 'shared ledger and log containers');
const css = strip(read('frontend/src/pages/ProofPage.css'));
ok(!/#[0-9a-f]{3,8}\b/iu.test(css), 'no hex colour');
ok(!/border-radius|font-family:\s*['"a-z]/iu.test(css.replace(/var\(--pg-[a-z-]+\)/gu, '')), 'no radius or font family literal');
ok(!/font-size:\s*\d/u.test(css), 'font sizes are tokens');
ok(!/\b(?!1px\b)\d+px\b/u.test(css.replace(/@media \(max-width: \d+px\)/gu, '')), 'no px literal except 1px rules and breakpoints');
ok(!/(^|[,}])\s*\.tg-[a-z_-]+\s*[,{]/mu.test(css), 'no top-level styles for shared .tg-* classes');

console.log(`frontend_proof_page: ${checks} checks passed`);
