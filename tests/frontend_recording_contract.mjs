import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const projectRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const read = (path) => readFileSync(resolve(projectRoot, path), 'utf8');
const appSource = read('frontend/src/App.jsx');
const analyticsSource = read('frontend/src/AnalyticsDashboard.jsx');
const labelsSource = read('frontend/src/operatorLabels.js');
const referenceSource = read('frontend/src/ReferencePanel.jsx');
const policySource = read('frontend/src/PolicyPanel.jsx');
const apiSource = read('frontend/src/api.js');
const scriptSource = read('docs/submission/video_script.md');
const quickstartSource = read('docs/submission/quickstart.md');
const aiContractTestSource = read('tests/frontend_ai_contract.mjs');

function requireText(source, text, context = text) {
  assert.ok(source.includes(text), `missing ${context}`);
}

function forbidText(source, text, context = text) {
  assert.equal(source.includes(text), false, `forbidden ${context}`);
}

function wordCount(value) {
  return value.match(/\b[\w’-]+\b/gu)?.length ?? 0;
}

const stableAppSelectors = [
  'data-testid="sandbox-connect"',
  'data-testid="aup-description"',
  'data-testid="aup-review"',
  'data-testid="aup-warning-dialog"',
  'data-testid="aup-return-to-edit"',
  'data-testid="invoice-confirm"',
  'data-testid="invoice-review"',
  'data-testid="invoice-create"',
  'data-testid="demo-burst"',
  'data-testid="velocity-filter"',
  'data-testid="velocity-grid"',
  'data-testid="velocity-selected-detail"',
  'data-testid="velocity-stage-status"',
  'data-testid="demo-dispute"',
  'data-testid="dispute-draft"',
  'data-testid="internal-review-zip-contents"',
  'data-testid="download-internal-review-zip"',
  'data-testid="dispute-approve"',
  'data-testid="dispute-result"',
  'testId="optional-toggle-analytics"',
];
for (const selector of stableAppSelectors) requireText(appSource, selector, `stable selector ${selector}`);
requireText(appSource, 'data-testid={`ai-generate-${stage}`}');
requireText(appSource, 'data-testid={testId}');

const aupSequence = [
  '>High-risk Claim<',
  '>Return to edit<',
  '>Standard Item<',
  '>Run Policy Check<',
  'No configured demo keyword matched',
  'data-testid="invoice-confirm"',
  '>Confirm Draft Context<',
  '>Create Sandbox draft<',
];
for (const marker of aupSequence) requireText(appSource, marker, `AUP recording control ${marker}`);

const aupInvalidator = appSource.match(/const invalidateAup = useCallback\(\(\) => \{([\s\S]*?)\n  \}, \[invalidateAi\]\);/u);
assert.ok(aupInvalidator, 'AUP invalidator exists');
for (const invalidation of [
  'setAup(null)',
  "setAupPhase('empty')",
  'setAupConsumed(false)',
  'setInvoiceReview(null)',
  'setInvoice(null)',
  'setInvoiceChecked(false)',
]) requireText(aupInvalidator[1], invalidation, `amount-change invalidation ${invalidation}`);

const amountEditor = appSource.match(/const editInvoiceAmount = \(value\) => \{([\s\S]*?)\n  \};/u);
assert.ok(amountEditor, 'invoice amount editor exists');
const postBindAmountEdit = amountEditor[1].match(/if \(invoiceReview \|\| invoice \|\| aupConsumed\) \{([\s\S]*?)\} else \{/u);
assert.ok(postBindAmountEdit, 'post-bind amount edit branch exists');
requireText(postBindAmountEdit[1], 'invalidateAup();', 'post-bind amount edit invalidates consumed AUP authority');
requireText(postBindAmountEdit[1], 'Run Policy Check again before confirming the draft context.', 'post-bind amount-change rerun notice');
const preBindAmountEdit = amountEditor[1].match(/\} else \{([\s\S]*?)\}\n    setInvoiceAmount\(value\);/u);
assert.ok(preBindAmountEdit, 'pre-bind amount edit branch exists');
for (const reset of ['setInvoiceReview(null)', 'setInvoice(null)', 'setInvoiceChecked(false)']) {
  requireText(preBindAmountEdit[1], reset, `pre-bind amount edit ${reset}`);
}
forbidText(preBindAmountEdit[1], 'invalidateAup()', 'pre-bind amount edit must preserve unconsumed AUP');
forbidText(preBindAmountEdit[1], 'setAup(', 'pre-bind amount edit must not mutate AUP result');
requireText(appSource, 'onChange={(event) => editInvoiceAmount(event.target.value)}', 'draft amount input uses the guarded editor');
requireText(appSource, 'disabled={disabled || !invoiceChecked || !aup || aupConsumed || description.length > 200}', 'draft context requires a fresh AUP result');
requireText(appSource, "disabled={disabled || !invoiceReview || !invoiceChecked || sandbox?.status !== 'connected'}", 'invoice creation requires a newly bound review');

for (const text of [
  'Filter transactions',
  'quickFilterText={velocityQuickFilter}',
  'onRowClicked={({ data }) => setSelectedVelocityTransaction(data)}',
  'Stage evidence checklist',
]) requireText(appSource, text);

const coreVelocityGrid = appSource.match(/<div className="transaction-grid" data-testid="velocity-grid"[\s\S]*?<\/div>/u);
assert.ok(coreVelocityGrid, 'core velocity grid exists');
requireText(coreVelocityGrid[0], 'loading={loading || !state}', 'AG Grid loading state prop');
requireText(coreVelocityGrid[0], 'overlayLoadingTemplate="Loading backend data"', 'AG Grid loading overlay');
requireText(coreVelocityGrid[0], 'overlayNoRowsTemplate="No transactions; inject a sales-burst scenario"', 'AG Grid no-row overlay');
forbidText(coreVelocityGrid[0], "overlayNoRowsTemplate={loading ?", 'no-row template must not encode loading state');
forbidText(coreVelocityGrid[0], 'Backend not connected; no transaction data', 'no-row template must remain deterministic');

for (const directPresentationLeak of [
  '{invoice.invoice_id}',
  '{invoice.evidence_receipt.proof_kind}',
  'separate GET readback',
  'Backend payload digest bound',
  '<Badge tone="muted">{brief.prompt_contract_id}</Badge>',
  '<Badge tone="muted">{brief.execution_evidence}</Badge>',
  '<strong>{draft.routing?.overall_state}</strong>',
  '>{row.requirement_state}</Badge>',
]) forbidText(appSource, directPresentationLeak);
requireText(appSource, 'Live Sandbox connection verified · credentials remain off-screen');
for (const reviewProof of [
  'Internal Review ZIP contents',
  'Six fixed files · generated locally · not sent to PayPal',
  'operatorLabel(receipt.reviewer)',
  'dateLabel(receipt.reviewed_at)',
  'operatorLabel(receipt.retention)',
]) requireText(appSource, reviewProof, `visible review proof ${reviewProof}`);
for (const providerContext of [
  'data-testid="provider-context"',
  "invoice?.evidence_receipt?.evidence_class === 'AUTHENTIC_SANDBOX_RESPONSE'",
  "['Sandbox seller country', 'Unconfirmed until Dashboard readback']",
  "['External action', 'Disabled by default; explicit Sandbox OAuth and unsent draft only']",
]) requireText(appSource, providerContext, `provider-context boundary ${providerContext}`);
requireText(appSource, 'Check capacity and tracking or delivery records; they are not supplied in this synthetic capture stream.',
  'Stage 2 reminder must not claim verified order proof');
requireText(appSource, 'This stage-level signal does not verify fulfillment evidence, classify this order as fraud, or predict any PayPal action.',
  'Stage 2 limits stay visible');
requireText(
  appSource,
  'onClick={() => { if (caseItem?.case_ref === item.case_ref) return; invalidateAi(); setSelectedCase(item.case_ref); setDraft(null); setReceipt(null); setReviewChecked(false); }}',
  'reselecting the reviewed case preserves its draft and receipt while a case change clears prior context',
);

const analyticsNavigation = appSource.match(/<a href="#analytics"[\s\S]*?>Grid analytics<\/a>/u);
assert.ok(analyticsNavigation, 'Grid analytics navigation action exists');
requireText(analyticsNavigation[0], 'setAnalyticsExpanded(true)', 'Grid analytics expands the workspace');
requireText(analyticsNavigation[0], 'setAnalyticsOpen(true)', 'Grid analytics launches the workspace in the same action');

for (const mappedCopy of [
  'Live Sandbox response',
  'Synthetic test run',
  'Draft · not sent',
  'No decision made',
  'Not established',
  'Ready for human review',
  'Item or service not received',
  'Requested from seller',
  'Prepare evidence',
  'Required fields present',
  'Live model response',
  'Local model response',
  'Reference only · no action authorized',
  'Draft details locked for this review',
  'No external action authorized',
]) requireText(labelsSource, mappedCopy, `mapped presentation copy ${mappedCopy}`);

for (const mappedUse of [
  'operatorLabel(aup.compliance_decision)',
  'operatorLabel(aup.current_policy_applicability)',
  'operatorLabel(draft.routing?.overall_state)',
  'operatorLabel(row.requirement_state)',
  'operatorLabel(brief.execution_evidence)',
]) requireText(appSource, mappedUse, `mapped presentation use ${mappedUse}`);

const zipBoundaryMatch = appSource.match(/data-testid="internal-review-zip-boundary"[\s\S]*?<\/p>/u);
assert.ok(zipBoundaryMatch, 'short Internal Review ZIP boundary exists');
const zipBoundary = zipBoundaryMatch[0]
  .replace(/<[^>]+>/gu, ' ')
  .replace(/\s+/gu, ' ')
  .trim();
assert.ok(wordCount(zipBoundary) <= 50, `ZIP boundary must remain short; received ${wordCount(zipBoundary)} words`);
for (const phrase of [
  'synthetic, pseudonymized preparation package',
  'not a PayPal-supported attachment',
  'does not prove authenticity, sufficiency, eligibility, completeness, or outcome',
  'nothing was submitted',
]) requireText(zipBoundary, phrase, `ZIP boundary phrase ${phrase}`);

for (const source of [appSource, analyticsSource]) {
  requireText(source, "timeZone: 'UTC'", 'fixed UTC rendering');
  requireText(source, 'UTC`', 'visible UTC suffix');
  assert.equal(/timeZone:\s*'(?!UTC)[^']+'/u.test(source), false, 'non-UTC timeZone is forbidden');
}
requireText(referenceSource, 'placeholder="YYYY-MM-DDTHH:mm:ssZ"');
requireText(policySource, 'Evaluation time (UTC ISO)');
requireText(scriptSource, 'Locked on: `2026-10-09 UTC`');
for (const [name, source] of [
  ['App', appSource],
  ['Analytics', analyticsSource],
  ['Reference panel', referenceSource],
  ['Policy panel', policySource],
  ['Video script', scriptSource],
  ['Quickstart', quickstartSource],
]) {
  for (const residue of ['+08:00', 'local time']) forbidText(source, residue, `${name} timezone residue ${residue}`);
}

requireText(analyticsSource, 'data-testid={`analytics-mobile-trigger-${id}`}');
for (const mobileId of ['lifecycle', 'pulse', 'stream', 'authority']) {
  requireText(analyticsSource, `id="${mobileId}"`, `mobile section ID ${mobileId}`);
}

for (const analyticsCopy of [
  'REVIEW ANALYTICS',
  'Review overview',
  'Transaction table',
  'Built with AG Grid Community and first-party React components. Synthetic session data only.',
  'Session storage: temporary',
]) requireText(analyticsSource, analyticsCopy);
for (const retiredCopy of [
  'AG GRID COMMUNITY · NO COMMERCIAL AG PACKAGES',
  'Open-source presentation boundary',
  'Judge view',
  'Inspect data',
  'Persistence: memory session',
]) forbidText(analyticsSource, retiredCopy);

requireText(scriptSource, 'Version: `VIDEO_SCRIPT_V3_LOCKED`');
requireText(scriptSource, 'VIDEO_SCRIPT_V1_LOCKED');
requireText(scriptSource, '9cc4c30eaabd49fd032d5f8101a4221bae226fef9e47319aca582ee4ac9f38df');
requireText(scriptSource, 'VIDEO_SCRIPT_V2_LOCKED');
requireText(scriptSource, '00b59c5dcbf0d2364dab3c68c1c1a8c6c4853e41d3cbfcdca59e4d32934abdd8');
for (const recordingInstruction of [
  'select **Return to edit**, choose **Standard Item**, and run the policy check again',
  'No match means only that no configured demo keyword matched; it does not mean compliant.',
  'Check **I reviewed the description and amount and confirm that this action creates a Sandbox draft only.**',
  'Select **Confirm Draft Context**, then **Create Sandbox draft**.',
  'sort and filter the transaction grid and open one evidence checklist',
  'Stage evidence checklist',
  'After a synthetic dispute opens, PayGuard reads its response deadline and requested seller evidence.',
  'The limited AI brief runs only after the rule checks.',
  'It receives approved synthetic facts and fixed source references',
  'Every status comes from validated workflow data. AG Grid lets reviewers inspect those signals',
  'address policy blind spots',
  'complete one current-byte live dress rehearsal',
  'Use a clean browser window with notifications disabled',
]) requireText(scriptSource, recordingInstruction, `V3 script contract ${recordingInstruction}`);

const firstSection = scriptSource.match(/## 0:00 to 0:15[\s\S]*?^> (.+)$/mu);
assert.ok(firstSection, 'opening spoken script exists');
const openingWords = wordCount(firstSection[1]);
assert.ok(openingWords <= 36, `opening must be at most 36 words; received ${openingWords}`);

const timedScript = scriptSource.split('## Locked five-point proof', 1)[0];
const spokenLines = timedScript.split('\n').filter((line) => line.startsWith('> ')).map((line) => line.slice(2));
const timedWords = spokenLines.reduce((total, line) => total + wordCount(line), 0);
assert.ok(timedWords >= 320 && timedWords <= 350, `timed spoken word count must remain within the rehearsable band; received ${timedWords}`);
requireText(scriptSource, `Timed spoken word count: \`${timedWords}\``);
const timedHeadings = [...scriptSource.matchAll(/^## (\d+):(\d+) to (\d+):(\d+) —/gmu)];
assert.equal(timedHeadings.length, 9, 'nine timed recording segments');
const lastHeading = timedHeadings.at(-1);
const finalSeconds = Number(lastHeading[3]) * 60 + Number(lastHeading[4]);
assert.ok(finalSeconds >= 1 && finalSeconds <= 179, `recording target must end within 1 to 179 seconds; received ${finalSeconds}`);

for (const proofPoint of [
  'One sanitized live PayPal Sandbox OAuth connection.',
  'One unsent Sandbox invoice draft, with no invoice identifier visible.',
  'One live bounded AI evidence brief.',
  'AG Grid transaction sorting, filtering, and one selected transaction card labelled as stage-level.',
  'Internal Review ZIP download followed by a recorded human review.',
]) requireText(scriptSource, proofPoint, `locked proof point ${proofPoint}`);

for (const quickstartLabel of [
  'High-risk Claim',
  'Return to edit',
  'Standard Item',
  'No demo rule matched',
  'No decision made',
  'Not established',
  'Confirm Draft Context',
  'Create Sandbox draft',
  'Filter transactions',
  'Stage evidence checklist',
  'Ready for human review',
  'Required fields present',
  'Review overview',
  'Transaction table',
  'Generate AI brief',
]) requireText(quickstartSource, quickstartLabel, `quickstart label ${quickstartLabel}`);

const nonEnglishCjkPattern = /[\u3400-\u9fff]|[\uFF1A\uFF0C\u3002\uFF08\uFF09]/u;
const retiredRegionPattern = new RegExp(`\\b(?:${'T' + 'W'}|${'Tai' + 'wan'})\\b`, 'iu');
for (const [name, source] of [
  ['App', appSource],
  ['Analytics', analyticsSource],
  ['Reference panel', referenceSource],
  ['Policy panel', policySource],
  ['Video script', scriptSource],
  ['Quickstart', quickstartSource],
]) {
  assert.equal(nonEnglishCjkPattern.test(source), false, `${name} contains non-English CJK text or punctuation`);
  assert.equal(retiredRegionPattern.test(source), false, `${name} contains a retired jurisdiction token`);
}

for (const rawContractMarker of [
  "'NOT_MADE'",
  "'NOT_ESTABLISHED'",
  "'NOT_EVALUATED'",
  "'SYNTHETIC_TEST_RESPONSE'",
  "'OPERATOR_LIVE_RESPONSE'",
  "'LOCAL_RUNTIME_RESPONSE'",
]) requireText(apiSource, rawContractMarker, `raw API contract marker ${rawContractMarker}`);
for (const preservedRawTest of [
  "compliance_decision: 'NOT_MADE'",
  "current_policy_applicability: 'NOT_ESTABLISHED'",
  "semantic_entailment: 'NOT_EVALUATED'",
  "execution_evidence: 'SYNTHETIC_TEST_RESPONSE'",
  "validLocal.execution_evidence = 'LOCAL_RUNTIME_RESPONSE'",
  "invalidLocalCloudEvidence.execution_evidence = 'OPERATOR_LIVE_RESPONSE'",
  "exportedEvidence.authority.provider_submission, 'NOT_PERFORMED'",
]) requireText(aiContractTestSource, preservedRawTest, `preserved raw API or export test ${preservedRawTest}`);

console.log(JSON.stringify({
  status: 'PASS',
  stable_selectors: stableAppSelectors.length + 1,
  mobile_ids: 4,
  opening_words: openingWords,
  timed_words: timedWords,
  target_seconds: finalSeconds,
  zip_boundary_words: wordCount(zipBoundary),
}));
