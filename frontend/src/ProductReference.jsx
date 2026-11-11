import { lazy, Suspense, useState } from 'react';
// Styles (ProductReference.css) load with CheckSaleExtras.jsx, which the Check a sale page mounts first (first-load budget).
import recordedSearches from './data/channel3_receipts_v1.json';

// Channel3 product reference: the seller picks which catalogue product is theirs, or none.
// Advisory only; the policy result above is never changed by it.
const STATUS_TEXT = {
  LOADING: 'Looking up your product in the Channel3 catalogue…',
  OFF: 'Product lookup is off (no Channel3 key on this console).',
  NOT_FOUND: 'Channel3 found no matching product. Describe the item in your own words in the listing.',
  NOT_SENT: 'Nothing safe to look up: the description has no product name left after removing personal details.',
  UNAVAILABLE: 'Product lookup is unavailable right now; the policy result is unaffected.',
};
// Recorded mode (hosted demo, no Channel3 key): only the recorded searches can be replayed, so say that instead
// of the "removing personal details" text, and name what can be tried.
const RECORDED_QUERIES = recordedSearches.receipts.map((receipt) => receipt.query);
const NOT_RECORDED_TEXT = `This demo replays ${RECORDED_QUERIES.length} recorded Channel3 searches and makes no live search call (card images still load from Channel3's image host). Try one of: ${RECORDED_QUERIES.join(' · ')}.`;

// (P3 2026-11-12, owner decision) Channel3 category reference under each card (CheckSaleExtras.jsx, on demand).
const CategoryReference = lazy(() => import('./CheckSaleExtras.jsx').then((module) => ({ default: module.CategoryReference })));

function Card({ card, selected, disabled, onPick }) {
  // A catalogue image can expire or fail to load (the hosted demo replays recorded results); show the plain tile then.
  const [imageFailed, setImageFailed] = useState(false);
  return (
    <li className={`product-card${selected ? ' is-selected' : ''}`} data-testid="product-card">
      {card.image_url && !imageFailed
        ? <img src={card.image_url} alt="" loading="lazy" referrerPolicy="no-referrer" onError={() => setImageFailed(true)} />
        : <span className="product-card-noimg" aria-hidden="true" data-testid="product-card-noimg" />}
      <div className="product-card-body">
        <strong>{card.title}</strong>
        <span className="product-card-meta">{[card.brand, card.category].filter(Boolean).join(' · ') || 'No brand or category listed'}</span>
        {card.key_features.length ? <ul className="product-card-features">{card.key_features.map((f) => <li key={f}>{f}</li>)}</ul> : null}
        {card.materials.length ? <span className="product-card-meta">Materials: {card.materials.join(', ')}</span> : null}
        <Suspense fallback={null}><CategoryReference category={card.category} /></Suspense>
      </div>
      <button type="button" className="product-card-pick" disabled={disabled} onClick={() => onPick(card.product_id)}
        aria-pressed={selected}>{selected ? 'Confirmed as my product' : 'This is my product'}</button>
    </li>
  );
}

export default function ProductReference({ result, confirmation, busy, onConfirm }) {
  if (!result) return null;
  const status = result.status;
  const source = result.source === 'channel3_recorded'
    // No search call is made; the product images still load from Channel3's image host (Q25).
    ? `Recorded Channel3 reply (${result.recorded_at.slice(0, 10)}), replayed: no search call; images load from Channel3`
    : 'Live Channel3 product search';
  return (
    <section className="product-reference" data-testid="product-reference" data-state={status} aria-live="polite">
      <div className="product-reference-head">
        <span className="meta-label">PRODUCT REFERENCE · CHANNEL3</span>
        {status === 'FOUND' ? <span className="product-reference-source">{source}</span> : null}
      </div>
      {status === 'FOUND' ? (
        <>
          <p>Pick the product you are selling. A confirmed card goes into the review ZIP as a record of what the item is, which helps if a buyer later says it was not as described.</p>
          <ul className="product-card-list">
            {result.cards.map((card) => <Card key={card.product_id} card={card} disabled={busy}
              selected={confirmation?.card?.product_id === card.product_id} onPick={onConfirm} />)}
          </ul>
          <div className="product-reference-foot">
            <button type="button" className="product-none" disabled={busy} onClick={() => onConfirm(null)}
              aria-pressed={confirmation?.choice === 'NONE_MATCH'}>{confirmation?.choice === 'NONE_MATCH' ? 'Marked: none of these' : 'None of these is my product'}</button>
            <span className="text-dim">Prices, shops and buy links from the catalogue are dropped. The policy result above is unchanged.</span>
          </div>
        </>
      ) : <p className="text-dim" data-testid="product-reference-status">{status === 'NOT_SENT' && result.reason === 'not_recorded' ? NOT_RECORDED_TEXT : STATUS_TEXT[status] || STATUS_TEXT.UNAVAILABLE}</p>}
    </section>
  );
}
