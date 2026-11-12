// "Sponsor map" in the console footer: each sponsor tool, what it does here, and the proof rows that involve it.
// The "what" text is copied word for word from docs/SPONSOR_TECH_MAP.md (checked by tests/frontend_sponsor_interactions.mjs).
// `proof` is the Proof page filter name (frontend/src/proof/proofData.js PROOF_SPONSORS); tools without proof rows link
// to the place they run instead. (fix r1 F7) AG Grid and Bryntum have no row in proof_facts_v1.json, so their links go
// to the all-orders grid and the deadline board; tests/frontend_fix_r1.mjs checks every `proof` entry has a row.
export const SPONSOR_MAP = Object.freeze([
  { name: 'AG Grid', what: 'Sortable and filterable transaction and case grids, quick filter, cell renderers, value formatters, tooltips, CSV export, lazy-loaded', href: '/#analytics' },
  { name: 'AG Charts', what: 'Bar and line series with cross-lines, legend and tooltip on a shared theme', href: '/#velocity' },
  { name: 'AG Studio', what: 'Evidence dashboard with a custom theme', href: '/dashboard.html' },
  { name: 'Bryntum', what: 'Evidence deadline board, one row per case', href: '/#evidence-board' },
  { name: 'Channel3', what: 'Product search for the seller-confirmed product reference card (goes into the review ZIP)', proof: 'Channel3' },
  { name: 'PayPal', what: 'OAuth, unsent invoice draft, dispute list and detail, and a gated provide-evidence send', proof: 'PayPal' },
  { name: 'Render', what: 'One free Docker web service from a Blueprint', proof: 'Render' },
  { name: 'Gemini', what: 'The guide’s AI step, the evidence brief and the Studio agent, each checked by code and capped per session', proof: 'Gemini' },
  { name: 'APIMatic', what: "The OpenAPI 3.1 description of the local console API (37 operations) passes APIMatic's validator with 0 errors", proof: 'APIMatic' },
  { name: 'Postman', what: 'A collection generated from that OpenAPI (37 requests, empty body skeletons, local console only)', proof: 'Postman' },
]);
export const sponsorHref = (entry) => (entry.proof ? `/proof.html#sponsor=${encodeURIComponent(entry.proof)}` : entry.href);
