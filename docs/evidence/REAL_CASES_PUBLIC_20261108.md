# Public Real-World PayPal Seller Dispute Cases (impact evidence for PayGuard)

Fetched: 2026-11-08. Scope: public web pages only; no login; no account touched.

## Method, source limits, privacy

- Source used: UK Financial Ombudsman Service (FOS) published final decisions (PDFs at financial-ombudsman.org.uk/decision/). Candidates came from two web searches; each decision URL was fetched once and its text read locally.
- Total network requests: 32 (budget 45): 2 searches, 23 FOS PDF fetches, 7 forum fetch attempts. Each URL requested once.
- Sources that could not be opened: PayPal Community (paypal-community.com), 6 thread URLs and 1 mirror host (ppl.i.lithium.com) failed with connection errors (ECONNREFUSED / ENOTFOUND). These are marked "could not open" and NOT used. Trustpilot was not attempted (no budget spent after the forum host refused connections). So this file contains FOS cases only: it covers (1) of the three requested source types.
- Excluded on purpose: FOS decisions already used by the project (DRN-3621543, DRN-5706769, DRN-3526295); FOS decisions fetched but where the complainant was a buyer with no seller-side evidence angle (DRN-5262863, DRN-5066876, DRN-6203486, DRN-4558316, DRN-3265188, DRN-5842790, DRN-3505698); decisions fetched only for metadata triage and not used (DRN-5620623, DRN-3795589).
- Privacy: no personal names, e-mails, account IDs, order numbers, addresses are recorded. Case IDs are the public FOS decision references. Summaries are paraphrased; at most one short quote (under 15 words) per case, attributed to the decision.
- "Inference" lines are my own reasoning, not statements in the sources.
- Selection bias: FOS only sees complaints after the customer is unhappy with PayPal's own outcome. Outcomes here are not representative of PayPal dispute outcomes in general.

## Cases

Result key: "Seller" = seller-side party prevailed; "PayPal" = PayPal's handling upheld, seller did not get what they wanted.

### RC-01 DRN-3778703 - Payment held for new seller
- Source: Financial Ombudsman Service decision. https://www.financial-ombudsman.org.uk/decision/DRN-3778703.pdf
- Date: decision 28 October 2022 (sale March 2022).
- Dispute type: Other (funds hold pending delivery confirmation; related to Item Not Received exposure).
- Seller evidence: seller supplied a tracking number and delivery date, but the proof showed collection from a post office, not delivery to an address, so it did not meet PayPal's basic proof-of-delivery elements (verifiable tracking, delivered status, recipient address matching shipping address).
- Result: Mixed. Hold judged fair (limited trading history, awaiting buyer confirmation); a small award was made only for poor customer service and unexplained delay.
- Inference: a pre-built proof-of-delivery check showing which of the required elements are missing, before upload, would have set the seller's expectation and prevented the "paid within a day" confusion.

### RC-02 DRN-5038521 - Business account limited, four open buyer claims closed for buyers
- Source: Financial Ombudsman Service decision. https://www.financial-ombudsman.org.uk/decision/DRN-5038521.pdf
- Date: decision 12 November 2024.
- Dispute type: Item Not Received (late or unsent orders) plus account limitation.
- Seller evidence: seller said items were sent with tracking, but the decision found orders were shipped late, buyers had to chase, and seller messages to buyers were slow. Decision notes seller protection could have been usable with valid proof of postage, but was suspended once the account was limited.
- Result: PayPal. Limitation fair; claims closed for buyers; funds hold of 180 days fair.
- Inference: timestamped dispatch proof plus a buyer-communication log prepared per order might have reduced the claim count that triggered the limitation.

### RC-03 DRN-3308660 - Seller wins after PayPal rejected buyer's receipt message
- Source: Financial Ombudsman Service decision. https://www.financial-ombudsman.org.uk/decision/DRN-3308660.pdf
- Date: decision 9 March 2022 (sale January 2021; response deadline in text 6 April 2022).
- Dispute type: Item Not Received (ITEM_NOT_RECEIVED style), after an earlier unauthorised-transaction claim that was not upheld.
- Seller evidence: postage-acceptance tracking only (no delivery scan; the postal provider said tracking was not updated during the pandemic), a postal-provider letter refunding postage, and a message from the buyer confirming receipt.
- Result: Seller (ombudsman upheld seller's complaint; reversed amount to be re-credited). PayPal had refused the buyer's message as acceptable evidence.
- Inference: assembling tracking gap explanation, carrier correspondence and buyer confirmation into one evidence pack in the first response window likely changes the outcome without a complaint.

### RC-04 DRN-5897525 - Seller lost chargeback despite proof of delivery
- Source: Financial Ombudsman Service decision. https://www.financial-ombudsman.org.uk/decision/DRN-5897525.pdf
- Date: decision 22 October 2025.
- Dispute type: Item Not Received via card chargeback (not a PayPal buyer-protection claim).
- Seller evidence: proof of delivery with a delivery picture, which PayPal forwarded to the card issuer; the item was dropped in a locker on 6 April, the chargeback was raised on 8 April, and delivery completed on 9 April (delivery came after the chargeback was raised).
- Result: PayPal. Chargeback lost, funds and dispute fee taken back; item-not-received chargebacks are excluded from seller protection.
- Inference: shipping timing evidence (dispatch before buyer chase, committed delivery window) is the item that most plausibly matters; the tool could also warn at listing time that this chargeback type is unprotected.

### RC-05 DRN-3293363 - Seller's courier "delivered" proof overturned by buyer evidence
- Source: Financial Ombudsman Service decision. https://www.financial-ombudsman.org.uk/decision/DRN-3293363.pdf
- Date: decision 13 April 2022 (purchase mid-2021).
- Dispute type: Item Not Received.
- Seller evidence: courier tracking saying delivered and received, accepted by PayPal initially. The ombudsman found the courier's own delivery photos showed a different door from the buyer's home, so the seller's evidence did not prove delivery.
- Result: Buyer (seller lost, via PayPal refund obligation).
- Inference: checking the delivery photo and address match before relying on "delivered" status, and requesting courier investigation early, would address the weak point.

### RC-06 DRN-5879609 (part A) - Wrong tickets sent
- Source: Financial Ombudsman Service decision. https://www.financial-ombudsman.org.uk/decision/DRN-5879609.pdf
- Date: decision 14 November 2025.
- Dispute type: Item Not Received (one buyer received nothing; another got extra).
- Seller evidence: none supporting dispatch to the claiming buyer; seller admitted the error and offered to fix it only after the claim.
- Result: PayPal. Refund recovered from seller; seller ineligible for seller protection; a 12-pound dispute fee applied per user agreement.
- Inference: an order-to-shipment reconciliation step before dispatch is the item that would have prevented the claim; evidence preparation could not.

### RC-07 DRN-5879609 (part B) - Friends-and-family payment charged back
- Source: same decision as RC-06. https://www.financial-ombudsman.org.uk/decision/DRN-5879609.pdf
- Date: decision 14 November 2025.
- Dispute type: Other (card chargeback on a payment accepted as friends and family; goods claimed not received).
- Seller evidence: the seller had no proof of postage for the goods.
- Result: PayPal. Chargeback lost; PayPal said it might reconsider if proof of postage was provided; no seller protection for this payment type.
- Inference: a stored proof-of-postage receipt per order is the single item that could have triggered reconsideration.

### RC-08 DRN-5666659 - Funds held 180 days after account blocked
- Source: Financial Ombudsman Service decision. https://www.financial-ombudsman.org.uk/decision/DRN-5666659.pdf
- Date: decision 23 July 2025.
- Dispute type: Other (account block and funds hold after a sale; no buyer claim existed).
- Seller evidence: none relevant; PayPal's risk reasoning was kept confidential and the ombudsman accepted it.
- Result: PayPal. Hold for 180 days judged fair because a buyer could still claim in that window.
- Inference: no dispute-evidence tool would likely change this outcome; it is a risk-review case, not an evidence case (included to show scope limits).

### RC-09 DRN-5720028 - Recipient lost chargeback on a "gift" payment
- Source: Financial Ombudsman Service decision. https://www.financial-ombudsman.org.uk/decision/DRN-5720028.pdf
- Date: decision 5 January 2026.
- Dispute type: Other (card chargeback claiming goods or services never received on a friends-and-family payment).
- Seller evidence: recipient submitted message screenshots saying it was a gift; PayPal forwarded them; card scheme ruled for the payer.
- Result: PayPal (account went negative after funds already withdrawn).
- Inference: written agreement or listing record showing a goods-or-services sale, captured before payment, is the item most likely to matter; payment-type choice itself decided seller protection.

### RC-10 DRN-5091323 - Account limited after many claims
- Source: Financial Ombudsman Service decision. https://www.financial-ombudsman.org.uk/decision/DRN-5091323.pdf
- Date: decision 4 December 2024.
- Dispute type: Item Not Received (partial non-delivery on a sale) plus account limitation.
- Seller evidence: the seller said she sent lots of evidence; the decision records an 80 pound partial refund to the buyer for undelivered items, and 14 protection claims in under four months.
- Result: PayPal. Limitation fair; seller had already withdrawn the funds so the later reversal left her owing.
- Inference: per-order delivery proof and a claim-rate dashboard might have kept claim volume under the threshold that triggered limitation.

### RC-11 DRN-3721889 - Seller's resale-screenshots refused in "not as described" dispute
- Source: Financial Ombudsman Service decision. https://www.financial-ombudsman.org.uk/decision/DRN-3721889.pdf
- Date: decision 27 September 2022 (sale September 2020).
- Dispute type: Not as Described (MERCHANDISE_OR_SERVICE_NOT_AS_DESCRIBED style).
- Seller evidence: seller submitted screenshots indicating the buyer was reselling the item at a higher price; PayPal told her this had no bearing. Return label used an outdated address on the seller's profile, so the returned item never reached her.
- Result: Seller in part. Ombudsman found PayPal should have considered the relevant evidence and awarded 100 pounds compensation; PayPal had already written off the negative balance.
- Inference: keeping the PayPal profile return address current, and filing evidence through the dispute channel with a clear relevance statement, are the two preparation items most likely to have shortened this case.

### RC-12 DRN-5746232 - Seller's tracking satisfied PayPal's four-part test
- Source: Financial Ombudsman Service decision. https://www.financial-ombudsman.org.uk/decision/DRN-5746232.pdf
- Date: decision 26 August 2025.
- Dispute type: Item Not Received.
- Seller evidence: online tracking with delivered status and date, plus recipient address matching the transaction details and showing city and postcode.
- Result: Seller. Buyer's complaint not upheld; the decision lists the four proof-of-delivery elements and finds all were met.
- Inference: this is the positive template: a checklist that confirms all four elements before submitting is the preparation that decides the case.

### RC-13 DRN-5724140 - Seller's valid-looking tracking overridden
- Source: Financial Ombudsman Service decision. https://www.financial-ombudsman.org.uk/decision/DRN-5724140.pdf
- Date: decision 30 July 2025.
- Dispute type: Item Not Received (high value, around 2,000 dollars).
- Seller evidence: courier tracking that met PayPal's proof-of-delivery definition.
- Result: Buyer (seller lost). Courier letter, email and a photo of the parcel in a shared hallway persuaded the ombudsman the parcel was not delivered to the buyer; PayPal ordered to refund the buyer.
- Inference: for high-value orders, delivery-photo and location verification (and signature where available) is the item that would have held up; tracking status alone proved fragile.

### RC-14 DRN-3323279 - Porch photo not accepted as proof of delivery
- Source: Financial Ombudsman Service decision. https://www.financial-ombudsman.org.uk/decision/DRN-3323279.pdf
- Date: decision 29 July 2022.
- Dispute type: Item Not Received (about 220 pounds).
- Seller evidence: tracking plus a photo of a parcel outside a door; the buyer lives in a block of flats with no porch.
- Result: Buyer (seller lost). Ombudsman found the seller's evidence did not show delivery to the buyer's address; 50 pounds compensation to the buyer; seller should have contacted the courier.
- Inference: a delivery photo that clearly ties to the address (building, door number, geotag) is the item that would have made the evidence usable.

### RC-15 DRN-3322417 - Courier later confirmed non-compliant delivery
- Source: Financial Ombudsman Service decision. https://www.financial-ombudsman.org.uk/decision/DRN-3322417.pdf
- Date: decision 30 May 2022 (delivery December 2021).
- Dispute type: Item Not Received (205 pounds, interest-free credit purchase).
- Seller evidence: courier tracking stating "delivered to porch" with a photo; this met PayPal's proof-of-delivery definition at the time, so the claim was closed for the seller.
- Result: Buyer (seller side lost). Decision says PayPal was entitled to decline on the terms but, after the courier later confirmed it was not delivered within its guidelines, fairness required a refund.
- Inference: proactively checking with the courier for delivery-guideline compliance (and raising the courier claim) before the claim window closes is the evidence step that would have mattered.

## Statistics (sample of 15 cases; small and not an incidence rate)

Dispute type (my classification of the primary dispute):
- Item Not Received: 9 (RC-03, 04, 05, 06, 10, 12, 13, 14, 15)
- Not as Described: 1 (RC-11)
- Other (holds, limitations, friends-and-family chargebacks): 5 (RC-01, 02, 07, 08, 09)
- Unauthorised, duplicate charge, refund not processed as primary type: 0

Outcome from the seller's side:
- Seller prevailed: 2 (RC-03, RC-12)
- Seller partly prevailed or mixed: 2 (RC-01, RC-11)
- Seller lost or PayPal's handling upheld: 11 (RC-02, 04, 05, 06, 07, 08, 09, 10, 13, 14, 15)
- Caveat: FOS sees only complaints already lost at PayPal, so this skews heavily toward seller losses. It says nothing about overall win rates.

Most frequently missing or weak evidence (count of cases where the decision text shows the gap):
- Delivery proof that is address-specific (delivered status, matching address, usable photo): 6 (RC-01, 05, 13, 14, 15, plus the tracking gap in RC-03)
- Seller-protection ineligibility not appreciated up front (chargeback INR, friends-and-family): 4 (RC-04, 07, 09, plus RC-06 for fees)
- Proof of dispatch or postage: 3 (RC-06, RC-07, RC-10)
- Timely handling or communication with buyers/courier: 2 (RC-02, RC-14)
- Not an evidence problem (risk/hold decisions): 1 (RC-08)
Counts overlap and are judgments from 15 documents; they are illustrations, not rates.

## Source access log

- FOS PDFs fetched and read: DRN-3778703, 5038521, 3308660, 3293363, 5897525, 5262863 (excluded, buyer), 5879609, 5666659, 5720028, 5091323, 3721889, 5746232, 5724140, 3323279, 3322417, 5066876, 4558316, 3265188, 5842790, 3505698, 5620623, 6203486, 3795589 (the last 8 for triage only).
- Could not open: 6 PayPal Community thread URLs, 1 mirror host (7 total). Trustpilot not attempted.
