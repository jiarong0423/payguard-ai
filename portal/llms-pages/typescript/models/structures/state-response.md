# State Response

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRlN0YXRlUmVzcG9uc2U

StateResponse.


# Interface Name

`StateResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `activity` | [`Activity[]`](http://localhost:3000/llms-pages/typescript/models/structures/activity.md) | Required | Activity. |
| `disputes` | [`DisputeSummary[]`](http://localhost:3000/llms-pages/typescript/models/structures/dispute-summary.md) | Required | Disputes. |
| `expiresAt` | `string` | Required | Expires at. |
| `policyVersion` | `string` | Required | Policy version. |
| `scenario` | [`Scenario`](http://localhost:3000/llms-pages/typescript/models/structures/scenario.md) | Required | Scenario. |
| `sessionId` | `string` | Required | Session id. |
| `source` | `string` | Required, Constant | Source.<br><br>**Value**: `'synthetic'` |
| `transactions` | [`Transaction[]`](http://localhost:3000/llms-pages/typescript/models/structures/transaction.md) | Required | Transactions. |
| `velocity` | [`VelocityResponse`](http://localhost:3000/llms-pages/typescript/models/structures/velocity-response.md) | Required | VelocityResponse. |


# Example

```ts
import {
  BaselineProvenanceEnum,
  StateResponse,
  Status14Enum,
  Status7Enum,
} from 'tradeglot-local-consolelib';

const stateResponse: StateResponse = {
  activity: [
    {
      at: 'at4',
      id: 'id8',
      kind: 'kind6',
      label: 'label8',
      source: 'synthetic',
    }
  ],
  disputes: [
    {
      caseRef: 'case_ref6',
      disputeAmount: {
        currencyCode: 'currency_code6',
        value: 'value0',
      },
      openedAt: 'opened_at0',
      orderRef: 'order_ref8',
      reason: 'reason2',
      sellerResponseDueDate: 'seller_response_due_date0',
      status: Status7Enum.NeedsReview,
    }
  ],
  expiresAt: 'expires_at6',
  policyVersion: 'policy_version8',
  scenario: {
    burst: false,
    dispute: false,
  },
  sessionId: 'session_id2',
  source: 'synthetic',
  transactions: [
    {
      amount: 'amount0',
      currency: 'currency8',
      occurredAt: 'occurred_at2',
      orderId: 'order_id2',
    }
  ],
  velocity: {
    advisoryOnly: 'True',
    alert: false,
    baselineAmountPerHour: 'baseline_amount_per_hour0',
    baselineProvenance: BaselineProvenanceEnum.SYNTHETICBASELINE,
    baselineWindowEnd: 'baseline_window_end2',
    baselineWindowStart: 'baseline_window_start4',
    currency: 'String7',
    currentAmountPerHour: 'current_amount_per_hour0',
    excludedFutureCount: 240,
    excludedPastCount: 132,
    limitations: [
      'limitations7'
    ],
    policyVersion: 'policy_version4',
    ratio: 'String5',
    status: Status14Enum.InsufficientBaseline,
    threshold: 'threshold4',
    totalAmount: 'total_amount2',
    transactionCount: 112,
    windowBoundary: 'left_open_right_closed',
    windowEnd: 'window_end6',
    windowHours: 2,
    windowStart: 'window_start8',
  },
};
```



