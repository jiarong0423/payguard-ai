// (r34 #1) The hosted demo's "Why?" text follows the guide API's own chooser status, the same value the guide's
// "Rules + Gemini" / "Rules only" badge reads (chooser_mode and model_requested from /guide/start and /guide/turn).
// The hosted guide uses Gemini only when the operator opted in (PAYGUARD_HOSTED_GUIDE_MODEL=gemini, backend
// guide_routes.py), capped at HOSTED_GUIDE_CALLS_PER_MINUTE and HOSTED_GUIDE_CALLS_PER_DAY; PayPal and the AI brief
// stay off in every case. Before any guide has started on this page the status is not known yet, so the text says
// so instead of claiming "Off".
export const HOSTED_GUIDE_CAPS = '5 a minute, 20 a day';

// `chooser`: null (no guide started yet) or { chooser_mode: 'keyword' | 'gemini', model_requested: boolean }.
export function hostedGeminiMode(chooser) {
  if (chooser?.chooser_mode === 'gemini') return 'gemini';
  if (chooser?.chooser_mode === 'keyword') return 'off';
  return 'unknown';
}

function baseHostedCopy(chooser) {
  const mode = hostedGeminiMode(chooser);
  if (mode === 'gemini') {
    return {
      mode,
      pill: 'Hosted demo · no PayPal calls',
      intro: `This public copy runs the same code with no PayPal keys, so it never calls PayPal. Only the guide may call Gemini, on the operator's free-tier key (${HOSTED_GUIDE_CAPS}); the evidence brief stays off.`,
      guides: 'Guides (rules + Gemini, capped) and recorded replays',
      local: 'Gemini evidence brief',
      gemini: `On for the guide only (${HOSTED_GUIDE_CAPS})`,
    };
  }
  if (mode === 'off') {
    return {
      mode,
      pill: 'Hosted demo · rules only · no PayPal calls',
      intro: "This public copy runs the same code with no keys. It never calls PayPal or Gemini, so no account or API credit is used.",
      guides: 'Guides in rules-only mode and recorded replays',
      local: 'Gemini evidence brief and Gemini guide',
      gemini: 'Off in hosted demo',
    };
  }
  return {
    mode,
    pill: 'Hosted demo · no PayPal calls',
    intro: `This public copy runs the same code with no PayPal keys, so it never calls PayPal. The guide may call Gemini only if the operator turned it on (${HOSTED_GUIDE_CAPS}); the guide's badge shows which. The evidence brief stays off.`,
    guides: 'Guides and recorded replays',
    local: 'Gemini evidence brief',
    gemini: `Start a guide to see it (guide only, at most ${HOSTED_GUIDE_CAPS})`,
  };
}

// `sandboxReads`: GET /connections said sandbox_reads (read-only Sandbox reads on). PayPal is then called for reads only;
// every write stays off. Without it the text above is returned unchanged.
// `sandboxSend`: GET /connections also said sandbox_send (owner decision 2026-11-10): the hosted demo may send dispute
// evidence to the owner's own Sandbox test disputes, once per dispute and per visit, at most 2 sends per address per day, under a shared cap.
export function hostedCopy(chooser, sandboxReads = false, sandboxSend = false) {
  const copy = baseHostedCopy(chooser);
  if (sandboxReads === true && sandboxSend === true) {
    return {
      ...copy,
      pill: 'Hosted demo · live Sandbox',
      intro: "This public copy uses the owner's PayPal Sandbox test account (never a live account). It reads Sandbox test disputes and, after your review and the send dialog, can send evidence built from the demo's synthetic seller records to one of them: once per dispute and once per visit (at most 2 sends per address per day), under a shared limit. Invoice drafts and tracking stay local-only.",
    };
  }
  // Not yet known (null): no claim either way; the pill never says "no PayPal calls" while the flag could still be on.
  if (sandboxReads === null) return { ...copy, pill: 'Hosted demo', intro: 'This public copy runs the same code. Its PayPal Sandbox mode is being checked.' };
  if (sandboxReads !== true) return copy;
  return {
    ...copy,
    pill: 'Hosted demo · read-only Sandbox',
    intro: 'This public copy only reads the PayPal Sandbox; it cannot write.',
  };
}
