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

export function hostedCopy(chooser) {
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
