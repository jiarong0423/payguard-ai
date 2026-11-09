# State Response

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRlN0YXRlUmVzcG9uc2U

StateResponse.


# Class Name

`StateResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `activity` | [`Array[Activity]`](http://localhost:3000/llms-pages/ruby/models/structures/activity.md) | Required | Activity. |
| `disputes` | [`Array[DisputeSummary]`](http://localhost:3000/llms-pages/ruby/models/structures/dispute-summary.md) | Required | Disputes. |
| `expires_at` | `String` | Required | Expires at. |
| `policy_version` | `String` | Required | Policy version. |
| `scenario` | [`Scenario`](http://localhost:3000/llms-pages/ruby/models/structures/scenario.md) | Required | Scenario. |
| `session_id` | `String` | Required | Session id. |
| `source` | `String` | Required, Constant | Source.<br><br>**Value**: `'synthetic'` |
| `transactions` | [`Array[Transaction]`](http://localhost:3000/llms-pages/ruby/models/structures/transaction.md) | Required | Transactions. |
| `velocity` | [`VelocityResponse`](http://localhost:3000/llms-pages/ruby/models/structures/velocity-response.md) | Required | VelocityResponse. |


# Example

```ruby
state_response = StateResponse.new(
  [
    Activity.new(
      'at4',
      'id8',
      'kind6',
      'label8',
      'synthetic'
    )
  ],
  [
    DisputeSummary.new(
      'case_ref6',
      SyntheticMoney.new(
        'currency_code6',
        'value0'
      ),
      'opened_at0',
      'order_ref8',
      'reason2',
      'seller_response_due_date0',
      Status7Enum::NEEDS_REVIEW
    )
  ],
  'expires_at2',
  'policy_version2',
  Scenario.new(
    false,
    false
  ),
  'session_id4',
  'synthetic',
  [
    Transaction.new(
      'amount0',
      'currency8',
      'occurred_at2',
      'order_id2'
    )
  ],
  VelocityResponse.new(
    'True',
    false,
    'baseline_amount_per_hour0',
    BaselineProvenanceEnum::SYNTHETIC_BASELINE,
    'baseline_window_end2',
    'baseline_window_start4',
    'String7',
    'current_amount_per_hour0',
    240,
    132,
    [
      'limitations7'
    ],
    'policy_version4',
    'String5',
    Status14Enum::INSUFFICIENT_BASELINE,
    'threshold4',
    'total_amount2',
    112,
    'left_open_right_closed',
    'window_end6',
    2,
    'window_start8'
  )
)
```



