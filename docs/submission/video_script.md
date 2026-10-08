# PayGuard AI Demonstration Script

Status: `LOCKED`

Version: `VIDEO_SCRIPT_V2_LOCKED`

Locked on: `2026-10-09 UTC`

Target duration: `2:45 to 2:55`

Timed spoken word count: `341`

## Version history

| Version | Status | Identity | Reason |
| --- | --- | --- | --- |
| `VIDEO_SCRIPT_V1_LOCKED` | Superseded | SHA-256 `9cc4c30eaabd49fd032d5f8101a4221bae226fef9e47319aca582ee4ac9f38df` | Replaced after the recording interaction inventory found an ambiguous AUP branch, a missing Stage 2 interaction, and judge-facing engineering terminology. |
| `VIDEO_SCRIPT_V2_LOCKED` | Current | The SHA-256 is recorded after this file is finalized. | Matches the exact AUP correction path, core transaction filtering, selected transaction card, UTC presentation, human-readable evidence labels, and five live proof points. |

Change control: wording, timing, claim boundaries, visible labels, click order, and the five required live proof points are frozen for the final recording. A later change requires a new version plus repeated timing, privacy, rights, claim-boundary, static-contract, and browser-rehearsal checks.

This final-take script requires the separately authorized PayPal Sandbox and bounded AI paths to be available during recording. If either live path is unavailable, stop the final take and repair the demonstration environment. Do not replace live execution with a prior result or operator-attested text.

Keep every visible merchant, transaction, and dispute record synthetic. Never show credentials, account identifiers, invoice identifiers, local paths, internal evidence folders, environment variables, or model prompts. Use only the PayGuard interface and the minimum sanitized Sandbox status needed to prove the integration.

## 0:00 to 0:15 — Problem, product, and lifecycle

Visual: Start on the compact PayGuard header. Flash three first-party cards: policy warning, fulfillment-record gap, and dispute deadline. Illuminate the three lifecycle stages. Do not show a fabricated PayPal limitation notice or third-party stock footage.

Spoken script:

> Sales spikes can hide policy warnings, missing fulfillment records, and dispute deadlines. PayGuard AI is the defensive buffer before provider review, surfacing evidence gaps while humans review and PayPal or external issuers retain final authority.

## 0:15 to 0:26 — Live Sandbox connection

Visual: With credentials already configured off-screen, expand **Optional PayPal US Sandbox connection**, select **Connect US Sandbox**, and show only **Live Sandbox connection verified** and **Live Sandbox response**. Keep the account, token, and technical receipt off-screen.

Spoken script:

> This demonstration connects live to PayPal Sandbox, with every credential kept off-screen.

## 0:26 to 0:55 — Stage 1: AUP correction path

Visual: Open **Pre-transaction / AUP Preflight Screen**. Select **High-risk Claim** and **Run Policy Check**. Show the `REVIEW_SIGNAL` warning and all three available choices: **Return to edit**, **Cancel flow**, and **Acknowledge and continue**. For the filmed branch, select **Return to edit**, choose **Standard Item**, and run the policy check again. Hold on **No demo rule matched**, **No decision made**, and **Not established**.

Spoken script:

> Before a draft, PayGuard checks the description against configured public-policy categories. A high-risk sample creates a review signal, not a verdict. The merchant can edit, cancel, or acknowledge. Here, we return to edit, choose the standard item, and rerun the check. No match means only that no configured demo keyword matched; it does not mean compliant.

## 0:55 to 1:10 — Human confirmation and unsent draft

Visual: Check **I reviewed the description and amount and confirm that this action creates a Sandbox draft only.** Select **Confirm Draft Context**, then **Create Sandbox draft**. Hold on **Sandbox invoice draft created**, **Draft · not sent**, and **Not submitted**. Confirm that no invoice identifier is visible.

Spoken script:

> After human confirmation, PayGuard locks this reviewed context and creates one unsent Sandbox invoice draft. The screen shows draft and not sent. No payment moves, and no production account is touched.

## 1:10 to 1:35 — Stage 2: velocity and fulfillment readiness

Visual: Open **Fulfillment / Velocity Guard** and select **Inject sales burst**. Show the backend-calculated ratio, synthetic baseline, comparison window, and UTC labels. In the core AG Grid, sort by **AMOUNT**, use **Filter transactions** to reduce the visible rows, clear the filter, and select one row. Hold on the selected transaction card and its **Stage evidence-readiness status** label.

Spoken script:

> During fulfillment, PayGuard compares synthetic captures with a declared local baseline. We sort and filter the core transaction grid and open one transaction in the evidence-readiness view. The selected card labels the status as stage-level; it does not classify the order or predict PayPal action.

## 1:35 to 2:03 — Stage 3: dispute evidence preparation

Visual: Select **Inject dispute**, open the synthetic case, and select **Generate evidence draft**. Show **Ready for human review**, **Proof of fulfillment**, **Requested from seller**, **Prepare evidence**, and **Required fields present**. Download **Internal Review ZIP**. Check the human-review box, select **Confirm local draft review**, and hold on **Local review recorded** and **Not submitted**.

Spoken script:

> After a synthetic dispute opens, PayGuard reads the case status and identifies the seller evidence requested in that record. It checks required fields, hides original identifiers, builds a timeline, and creates the pseudonymized Internal Review ZIP. This is a local preparation package, not a PayPal-supported attachment. We download it and record the human review. Nothing is submitted.

## 2:03 to 2:25 — Live bounded AI brief

Visual: In the dispute stage, select **Generate AI brief** once. Show the live model identity, mapped execution label, one evidence point, one missing item, fixed source references, and **HUMAN REVIEW REQUIRED**. Keep the prompt, key, raw response, and technical identifiers off-screen.

Spoken script:

> The bounded AI runs only after the rule checks. It receives approved synthetic facts and fixed source references, then summarizes one evidence point and one missing item. It cannot change a rule result, call a payment tool, submit evidence, or decide the dispute.

## 2:25 to 2:45 — AG Grid analytics and authority

Visual: Select **Grid analytics** to open the AG Grid Community workspace. Hold on **Review overview**, the three-stage review path, authority map, evidence counts, and transaction table. Keep expert policy panels and technical details collapsed.

Spoken script:

> Every status comes from validated workflow data. AG Grid lets reviewers inspect those signals, while the interface keeps decision authority visible at every stage. PayGuard prepares facts and exposes gaps; PayPal or the external issuer makes the final decision.

## 2:45 to 2:55 — Close

Visual: Return to the three-stage Defense Buffer and finish on the PayGuard wordmark with all three stages visible.

Spoken script:

> PayGuard does not replace provider review. It gives merchants more time to address policy blind spots, complete fulfillment records, and prepare dispute evidence.

## Locked five-point proof

The final take must visibly contain all five items:

1. One sanitized live PayPal Sandbox OAuth connection.
2. One unsent Sandbox invoice draft, with no invoice identifier visible.
3. One live bounded AI evidence brief.
4. AG Grid transaction sorting, filtering, and one selected transaction card labelled as stage-level.
5. Internal Review ZIP download followed by a recorded human review.

## Operator run sheet

1. Start a fresh backend before the take so every stage has its one available AI attempt.
2. Confirm the browser, API, and Sandbox status without exposing a terminal, environment variable, account identifier, or credential.
3. Reset synthetic demo data.
4. Expand the Sandbox section and connect live.
5. Run the exact high-risk to edit to standard-item AUP path.
6. Check the human confirmation, confirm the draft context, and create exactly one unsent draft.
7. Inject the sales burst, sort, filter, clear the filter, and select one core-grid row.
8. Inject the dispute, generate the draft, download the Internal Review ZIP, and record the local human review.
9. Generate exactly one dispute-stage bounded AI brief.
10. Open Grid analytics for the final architecture and authority frame.
11. Stop the take if a credential, identifier, raw prompt, local path, unexpected error, or provider failure appears.

## Locked positioning

Use this wording in the Devpost description:

> PayGuard AI is a defensive buffer layer between merchant operations and provider review workflows. Rule checks surface evidence gaps; bounded AI summarizes approved facts; AG Grid makes the review state visible. Humans remain in control, and PayPal or external issuers retain final authority.

Do not claim that PayGuard prevents a freeze, predicts a provider threshold, guarantees a dispute result, declares an activity compliant, produces an officially accepted evidence package, or sends evidence to a provider. Do not call the Internal Review ZIP an official PayPal evidence format or a PayPal-ready ZIP. Do not claim that `NO_MATCH` means compliant, allowed, approved, legal, or safe. Do not claim a percentage of competing projects without a verified competition dataset.

## Required final checks

- The finished public YouTube video is between 1 and 179 seconds.
- The recording contains every item in the locked five-point proof.
- The visible repository, license, interface, narration, and captions are English.
- Every visible timestamp is labelled UTC.
- No credential, account identifier, invoice identifier, local path, environment variable, prompt, or private evidence appears.
- No statement claims that PayGuard prevents or predicts holds, limitations, reserves, disputes, or losses.
- No statement calls an item compliant, prohibited, approved, legal, or safe.
- The Internal Review ZIP is described only as a local preparation package and never as a PayPal-supported attachment or official submission format.
- No third-party music, marks, stock footage, or other copyrighted material appears without recorded permission.
- The final cut shows the product functioning end to end and matches the public repository behavior.
