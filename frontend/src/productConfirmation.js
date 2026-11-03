// The seller's Channel3 product confirmation, kept in its own state.
//
// The AUP evaluation expires after two minutes and the console then clears the check result. The product
// confirmation must outlive that: the seller confirmed which catalogue product the item is, and the review ZIP
// records it later. It is cleared only when its basis changes:
//   description_edited   the seller changed the text the card was confirmed for
//   policy_check         a new policy check starts (new evaluation, new cards)
//   session_changed      a new, expired or reset demo session
// AUP expiry is deliberately not a reason. Every clear bumps a revision; a confirmation reply is accepted only if
// it was requested at the current revision and for the current session, so a reply that arrives after an edit,
// a new check or a session change is dropped instead of reattaching a stale card.

export const CLEAR_REASONS = Object.freeze(['description_edited', 'policy_check', 'session_changed']);

export const initialProductConfirmation = Object.freeze({ record: null, revision: 0, session: null });

export function productConfirmationReducer(state, action) {
  switch (action?.type) {
    case 'clear':
      if (!CLEAR_REASONS.includes(action.reason)) return state;
      return { record: null, revision: state.revision + 1, session: action.reason === 'session_changed' ? (action.session ?? null) : state.session };
    case 'confirmed':
      if (action.revision !== state.revision || action.session !== state.session || !action.record) return state;
      return { ...state, record: action.record };
    default:
      return state;
  }
}
