// (r31 J5 A6) The server's single-use send confirmation (r30 J2 P2-1), kept per kind on the console side.
// The send dialog's re-check preview returns a confirm_token; the send that follows carries that token and nothing
// else. An evidence token never goes with a tracking send (or the other way round), a send uses its token once, and
// Reset demo or a new session drops both. A re-check without a token leaves null, which the server refuses with
// 409 confirmation_required, so a missing token can never look like a confirmed send.
export const SEND_KINDS = Object.freeze(['evidence', 'tracking']);

const kindOf = (kind) => (kind === 'tracking' ? 'tracking' : 'evidence');
const tokenOf = (recheck) => (typeof recheck?.confirm_token === 'string' && recheck.confirm_token ? recheck.confirm_token : null);

// (r32 J5 P3-1) The server issues a token only when the send could go out. A re-check preview that says the send is
// ready (switch on, Sandbox source, frozen payload) but carries no token is a failed re-check: the dialog closes
// with this notice instead of starting the countdown towards a send the server would refuse with 409.
export const MISSING_CONFIRM_NOTICE = 'Could not get a send confirmation from the server; prepare the preview again. Nothing was sent.';
export function readyWithoutToken(recheck) {
  return recheck?.submit_flag_enabled === true && recheck?.source === 'paypal_sandbox' && recheck?.external_send === 'FROZEN'
    && tokenOf(recheck) === null;
}

export function createSendConfirmTokens() {
  const tokens = { evidence: null, tracking: null };
  return {
    // The dialog's latest re-check replaces the earlier token of the same kind only.
    remember(kind, recheck) { tokens[kindOf(kind)] = tokenOf(recheck); },
    // The submit body: the request fields plus submit: true and this kind's token (null when there is none).
    submitBody(kind, fields) { return { ...fields, submit: true, confirm_token: tokens[kindOf(kind)] }; },
    // After a send, whatever its result: the server used the token up or refused it, so it is never sent again.
    clear(kind) { tokens[kindOf(kind)] = null; },
    // Reset demo or a new session.
    clearAll() { tokens.evidence = null; tokens.tracking = null; },
    peek(kind) { return tokens[kindOf(kind)]; },
  };
}
