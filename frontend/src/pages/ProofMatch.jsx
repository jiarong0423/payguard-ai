// (J-A item 8, judge B #6, 2026-11-12) A small "Matches Proof" stamp for a step page's result area: it links to the Proof
// row (proof.html#row-<id>) that records the same flow. Display only; the row must exist in proof_facts_v1.json, or
// nothing is drawn (a stamp never points at a row that is not there). Its hover text is the row's own "proven" sentence.
// Placement in Check a sale, Sales spike and Disputes belongs to those pages' owners (ui_mock/reviews/J_requests.md).
import facts from '../data/proof_facts_v1.json';
import { STATUS, SpriteIcon } from '../theme/iconMap.js';

// (K8 arbitration) On demo data the stamp is a neutral tag ("Demo data · see Proof row"), so it never reads as verified.
export default function ProofMatch({ row, demo = false }) {
  const item = facts.rows.find((entry) => entry.id === row);
  if (!item) return null;
  if (demo) return <a className="tg-tag" href={`/proof.html#row-${item.id}`} data-testid="proof-match" data-proof-row={item.id} data-demo="true" title={`Proof row: ${item.proven}`}>Demo data · see Proof row</a>;
  return <a className="tg-stamp tg-stamp--ok" href={`/proof.html#row-${item.id}`} data-testid="proof-match" data-proof-row={item.id} title={`Proof row: ${item.proven}`}><SpriteIcon name={STATUS.ok} size="sm" />Matches Proof</a>;
}
