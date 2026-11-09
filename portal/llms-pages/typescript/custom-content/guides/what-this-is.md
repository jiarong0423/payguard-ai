# what-this-is

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/cGFnZSUzQWd1aWRlcyUyRndoYXQtdGhpcy1pcw

TradeGlot gives small PayPal sellers rule checks and a gated evidence workflow. Everything in this API documentation describes the **local console** (127.0.0.1:8000) and runs on **synthetic data** against the **PayPal Sandbox**.


# Safe by design

- Advisory only: every answer is a review signal. It is not a compliance decision and not legal advice.
- A person approves every send: one tick, then two presses. The hosted demo makes no PayPal calls and answers `503 hosted_demo_disabled` on every route that would.
- The AI step (Gemini) only picks from closed options and its picks are checked by rules. It does not guess and does not decide who wins.
- PayPal and the card issuer make every real decision.


# Where to go next

- Browse the endpoint groups on the left. Each one says whether the hosted demo answers it.
- Agents can use the same rule checks through the read-only MCP server: see the next guide.



