# PayGuard AI Demonstration Script

Status: `LOCKED` pre-edit recording plan; the final public video is [2:02](https://youtu.be/K28N9QhRp1E).

Version: `VIDEO_SCRIPT_V10_LOCKED`

Locked on: `2026-10-10 UTC`

Original target duration: `2:40 to 2:50`. These scene timestamps belong to the recording plan, not the edited video's seek positions.

Timed spoken word count: `294`

## Version history

| Version | Status | Identity | Reason |
| --- | --- | --- | --- |
| `VIDEO_SCRIPT_V1_LOCKED` | Superseded | SHA-256 `9cc4c30eaabd49fd032d5f8101a4221bae226fef9e47319aca582ee4ac9f38df` | Replaced after the recording interaction inventory found an ambiguous AUP branch, a missing Stage 2 interaction, and judge-facing engineering terminology. |
| `VIDEO_SCRIPT_V2_LOCKED` | Superseded | SHA-256 `00b59c5dcbf0d2364dab3c68c1c1a8c6c4853e41d3cbfcdca59e4d32934abdd8` | Replaced after independent recording review found an opening-frame mismatch and two judge-facing proof gaps. |
| `VIDEO_SCRIPT_V3_LOCKED` | Superseded | SHA-256 `a9237f3256e6c3565a116dfe48fbf05e34b69dad608966a678dce48cad738a15` | Aligned the opening with the visible lifecycle cards, listed the six ZIP members, recorded an explicitly unauthenticated demo review with UTC time, and preserved the five live proof points. |
| `VIDEO_SCRIPT_V4_LOCKED` | Superseded | SHA-256 `07d2421431b6af7b79bfcdc4c8cece744a7a97bd5d1ca5fa51ad2b4a61c7fa4d` | Named the PayPal Sandbox, AG Grid and bounded AI proof in the first 15 seconds, but omitted the confirmation action that opens the AUP warning dialog. |
| `VIDEO_SCRIPT_V5_LOCKED` | Superseded | SHA-256 `0ce4a87ceb13b2e8e98c8cde03ec32051e25727cd1767b78dfdc70cd17b08aae` | Preserved the correct AUP warning-dialog click order but left the recording model route unnamed and only five seconds below the video limit. |
| `VIDEO_SCRIPT_V6_LOCKED` | Superseded | SHA-256 `1b7d2afbacaf8f9f5ded39e4f7a8c7f68858d3382184ce1f1948cbba4022c688` | Names Gemini API as the single live recording adapter, keeps Nemotron 4B as a separate alternative, and gives the AG Grid interaction more continuous screen time. |
| `VIDEO_SCRIPT_V7_LOCKED` | Superseded | SHA-256 `40b693425f88d82b5ff81da98ff3019431622aecbbacb5a1c11023434cd06cc5` | Uses the approved merchant-view synthetic hero cover; timing, narration and live proof remain unchanged from V6. |
| `VIDEO_SCRIPT_V8_LOCKED` | Superseded | SHA-256 `e317b741006c5ab9f7a236baf60a5199b52b7ae8a97ad6a4279acece998cd796` | Adds the requested second PNG workflow image after the live analytics proof; timing, narration and all five live proof points remain unchanged. |
| `VIDEO_SCRIPT_V9_LOCKED` | Superseded | SHA-256 `536a3a8bfa68d12eb5fb8ca03c8121ea009a86f1dad52cf66c5fbfb3a08f855b` | Superseded after the UI changed to a focused one-stage view with new control labels and on-demand evidence details. |
| `VIDEO_SCRIPT_V10_LOCKED` | Final recording plan; public cut is 2:02 | Bind this document to the next validated public export manifest. | Aligns clicks with the focused UI. The edited video is shorter than this plan; verify claims against the video itself. |

Change control: wording, timing, claim boundaries, visible labels, click order, and the five required live proof points are frozen for the final recording. A later change requires a new version plus repeated timing, privacy, rights, claim-boundary, static-contract, and browser-rehearsal checks.

This final-take script selects the default Gemini API backend (`./tools/run.sh api`) and requires the separately authorized PayPal Sandbox and bounded AI paths to be available during recording. It shows one live `gemini-3.8-flash` dispute-stage brief after all three synthetic scenarios. It does not claim a combined three-stage AI result. If either live path is unavailable, stop the final take and repair the demonstration environment. Do not replace live execution with a prior result or operator-attested text.

The default-off `nvidia-nemotron-3-nano-4b` LM Studio route (`./tools/run.sh local-ai-api`) is documented on a separate local-model option slide, outside the timed video. The slide shows only one manually observed synthetic AUP response; it does not prove a three-stage adapter run. Other local models require the same adapter, schema, and closed-output validation before use. It is not Gemini, an automatic fallback, a second call in this take, or a distributed production deployment. The operator selects exactly one backend at process start; the browser cannot change it. This V10 final take remains on Gemini API.

Keep every visible merchant, transaction, and dispute record synthetic. Never show credentials, account identifiers, invoice identifiers, local paths, internal evidence folders, environment variables, or model prompts. Use only the PayGuard interface and the minimum sanitized Sandbox status needed to prove the integration.

## 0:00 to 0:15 — Problem, product, and lifecycle

Visual: Start on the working PayGuard console for three seconds. Show the [cover](payguard_cover.png) for five seconds so the three lifecycle stages and their tools are legible, then return to the working console. The [second image: three-stage workflow map](payguard_judge_overview.png) appears only after the live analytics proof near the end. The cover is a synthetic merchant-side concept illustration, not a product screenshot; show the Sandbox, AG Grid and Gemini API executions live in their timed segments. Do not show a fabricated PayPal limitation notice or third-party stock footage.

Spoken script:

> Policy warnings. Sudden sales. Dispute deadlines. PayGuard AI connects a PayPal Sandbox draft, AG Grid evidence review, and one bounded Gemini API brief. Merchants review; PayPal and issuers decide.

## 0:15 to 0:25 — Live Sandbox connection

Visual: With credentials already configured off-screen, expand **Optional PayPal US Sandbox connection**, select **Connect US Sandbox**, and show only **Live Sandbox connection verified** and **Live Sandbox response**. Keep the account, token, and technical receipt off-screen.

Spoken script:

> First, we verify a live PayPal Sandbox connection with every credential kept off-screen.

## 0:25 to 0:55 — Stage 1: AUP correction path

Visual: Stay in **STEP 01 AUP preflight**. Select **High-risk Claim** and **Run Policy Check**. Show the review signal. In **Optional PayPal US Sandbox connection**, check **I reviewed the description and amount and confirm that this action creates a Sandbox draft only.**, then select **Confirm Draft Context**. The warning dialog now opens; show **Return to edit**, **Cancel flow**, and **Acknowledge and continue**. For the filmed branch, select **Return to edit**, choose **Standard Item**, and run the policy check again. Hold on **No demo rule matched**; expand **How this result was checked** only if time permits to show **No decision made** and **Not established**.

Spoken script:

> For the first input, we choose a high-risk description. The US policy check raises a review signal, not a verdict. We confirm draft context to show three merchant choices: edit, cancel, or acknowledge. We return to edit, choose the standard item, and check again. No match means only that no configured demo keyword matched; it does not mean compliant.

## 0:55 to 1:08 — Human confirmation and unsent draft

Visual: **Return to edit** cleared the earlier confirmation. Check **I reviewed the description and amount and confirm that this action creates a Sandbox draft only.** again. Select **Confirm Draft Context**, then **Create Sandbox draft**. Hold on **Sandbox invoice draft created**, **Draft · not sent**, and **Not submitted**. Confirm that no invoice identifier is visible.

Spoken script:

> Editing cleared the previous confirmation. We confirm the revised context and create one unsent Sandbox invoice draft. No payment moves.

## 1:08 to 1:43 — Stage 2: velocity and fulfillment readiness

Visual: Select **Next: sales burst**; the prior stage closes and STEP 02 scrolls into view. Select **Load sales burst**. Show the ratio, capture count and alert. Briefly expand **How this signal was calculated** for the synthetic baseline, comparison window and UTC labels, then close it. In the core AG Grid, sort by **AMOUNT**, use **Filter transactions** to reduce the visible rows, clear the filter, and select one row. Hold on the selected transaction card and its **Stage evidence checklist** label.

Spoken script:

> For the second input, we load a synthetic sales burst. PayGuard compares the capture window with a declared baseline. We sort and filter the transaction grid in AG Grid and open one selected order's evidence checklist. This stage-level signal asks for fulfillment review; it cannot predict a PayPal hold or classify that order as fraud.

## 1:43 to 2:15 — Stage 3: dispute evidence preparation

Visual: Select **Next: dispute evidence**; STEP 02 closes and STEP 03 scrolls into view. Select **Load dispute case**, open the synthetic case, and select **Prepare evidence draft**. Show the UTC response deadline and response readiness. Briefly expand **Evidence fields, requested items, and ZIP contents** to show the requested seller proof and six ZIP members, then close it. Select **Download review ZIP**. Insert [the verified local ZIP slide](payguard_zip_review_slide.png) for four seconds; it shows the six archive members and the internal-review boundary. Then check the human-review box and select **Confirm local draft review**. Hold on the local review receipt, UTC review time, session-only retention, and **Not submitted**.

Spoken script:

> For the third input, we load a synthetic dispute. PayGuard shows the response deadline and requested seller proof. It checks required fields, builds a timeline, and replaces original identifiers in an Internal Review ZIP. We download this six-file local package and record a human review. It is not a PayPal-supported attachment; nothing is submitted.

## 2:15 to 2:35 — Live bounded Gemini API brief

Visual: In the dispute stage, select **Generate AI brief** once on the already selected Gemini API backend and begin narration with that click. Keep the same take through the loading state and result; only idle waiting frames may be trimmed. Show `gemini-3.8-flash`, **Live model response**, one evidence point, one missing item, fixed source references, and **HUMAN REVIEW REQUIRED**. Keep the prompt, key, raw response, and technical identifiers off-screen. This is a dispute-stage brief, not a merged conclusion about all three scenarios.

Spoken script:

> After rule checks, one bounded Gemini call. It reads fixed synthetic facts and pinned sources, then highlights an evidence point and missing item. It cannot change rules, submit evidence, or decide disputes; a person reviews.

## 2:35 to 2:44 — AG Grid analytics and authority

Visual: Select **Grid analytics** to open the AG Grid Community workspace. Hold on **Review overview**, the three-stage review path, authority map, evidence counts, and transaction table until 2:42. Then show the second image, [three-stage workflow map](payguard_judge_overview.png), for two seconds as a visual recap. Keep expert policy panels and technical details collapsed.

Spoken script:

> The analytics view links all three stages while keeping PayPal and issuer authority explicit.

## 2:44 to 2:50 — Close

Visual: Return to the working Defense Buffer and finish on the PayGuard wordmark with the three stage tabs visible.

Spoken script:

> PayGuard gives merchants more time to inspect gaps and prepare evidence before provider review.

## Shot cue sheet for editing

These are target cut points, not measured provider latency. Keep action initiation and its resulting state in the same take. The local-model option slide is outside this timed video.

| Time | On-screen material and exact action | Proof to hold |
| --- | --- | --- |
| 0:00–0:03 | Working PayGuard three-stage console | Real product opens the film |
| 0:03–0:08 | `payguard_cover.png` | Merchant-view concept of three stages and PayPal Sandbox, AG Grid, Gemini API tools |
| 0:08–0:15 | Working console and stage navigation | Defense Buffer path before the first click |
| 0:15–0:25 | Expand Sandbox section; select **Connect US Sandbox** | Sanitized live connection status |
| 0:25–0:36 | **High-risk Claim** → **Run Policy Check** | `REVIEW_SIGNAL`, not a verdict |
| 0:36–0:45 | Check draft-only confirmation → **Confirm Draft Context** | Three warning-dialog choices visible |
| 0:45–0:55 | **Return to edit** → **Standard Item** → **Run Policy Check** | No demo rule matched, no decision made |
| 0:55–1:08 | Recheck confirmation → **Confirm Draft Context** → **Create Sandbox draft** | Draft created, unsent and not submitted |
| 1:08–1:18 | **Next: sales burst** → **Load sales burst** | Prior stage closes; synthetic ratio and captures appear |
| 1:18–1:35 | AG Grid sort → filter → clear filter | Live grid interaction remains on screen |
| 1:35–1:43 | Select one transaction row | Stage evidence checklist, not an order verdict |
| 1:43–1:55 | **Next: dispute evidence** → **Load dispute case** → open case → **Prepare evidence draft** | Prior stage closes; deadline and review status appear |
| 1:55–2:05 | Open evidence details briefly → **Download review ZIP** | Six members and local package boundary |
| 2:05–2:09 | `payguard_zip_review_slide.png` | Verified six-file local archive; internal review only |
| 2:09–2:15 | Check review box → **Confirm local draft review** | Human review, UTC time and not submitted |
| 2:15–2:35 | Select **Generate AI brief** once | Live `gemini-3.8-flash` result and human-review status |
| 2:35–2:42 | Open **Grid analytics** | Live three-stage path and authority map |
| 2:42–2:44 | `payguard_judge_overview.png` | Second static image recaps the three stages and human/provider boundary |
| 2:44–2:50 | Return to working Defense Buffer and wordmark | Closing value line |

Timing sensitivity: the AUP correction branch has five visible decisions in 30 seconds, and the 20-second Gemini segment includes unknown live network latency. The 2:50 target leaves up to nine seconds before the 2:59 maximum; a delayed or failed provider response requires a new take, not an edited prior response.

## Locked five-point proof

The final take must visibly contain all five items:

1. One sanitized live PayPal Sandbox OAuth connection.
2. One unsent Sandbox invoice draft, with no invoice identifier visible.
3. One live bounded Gemini API dispute evidence brief, showing `gemini-3.8-flash` and **Live model response**.
4. AG Grid transaction sorting, filtering, and one selected transaction card labelled as stage-level.
5. Internal Review ZIP download followed by a recorded human review.

## Operator run sheet

1. Before recording, complete one current-byte live dress rehearsal; do not describe one or two samples as latency percentiles. Start the default Gemini backend with `./tools/run.sh api` and restart it before the final take so the dispute stage has its one available AI attempt. Do not start the local-model backend for this take.
2. Use a clean browser window with notifications disabled, one neutral tab visible, and download UI hidden. Confirm the API and Sandbox status without exposing a terminal, environment variable, account identifier, credential, or local download path.
3. Reset synthetic demo data.
4. Expand the Sandbox section and connect live.
5. Run the exact high-risk to edit to standard-item AUP path.
6. Check the human confirmation, confirm the draft context, and create exactly one unsent draft.
7. Select **Next: sales burst**, load the sales burst, sort, filter, clear the filter, and select one core-grid row.
8. Select **Next: dispute evidence**, load the dispute case, prepare the draft, download the review ZIP, and record the local human review.
9. Generate exactly one live dispute-stage Gemini API brief and verify the visible Gemini model and live-response labels.
10. Open Grid analytics for the final architecture and authority frame; show the second PNG only after this live view.
11. Cut only idle loading time while retaining the initiation and resulting state from the same take. Stop the take if a credential, identifier, raw prompt, local path, unexpected error, or provider failure appears. Do not switch to Nemotron 4B or automatically retry Gemini during the take.

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
