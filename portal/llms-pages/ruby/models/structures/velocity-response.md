# Velocity Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRlZlbG9jaXR5UmVzcG9uc2U

VelocityResponse.


# Class Name

`VelocityResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `advisory_only` | `String` | Required, Constant | Advisory only.<br><br>**Value**: `'True'` |
| `alert` | `TrueClass \| FalseClass` | Required | Alert. |
| `baseline_amount_per_hour` | `String` | Required | Baseline amount per hour. |
| `baseline_provenance` | [`BaselineProvenanceEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/baseline-provenance.md) | Required | Baseline provenance. |
| `baseline_window_end` | `String` | Required | Baseline window end. |
| `baseline_window_start` | `String` | Required | Baseline window start. |
| `currency` | String | Required | This is a container for any-of cases. |
| `current_amount_per_hour` | `String` | Required | Current amount per hour. |
| `excluded_future_count` | `Integer` | Required | Excluded future count. |
| `excluded_past_count` | `Integer` | Required | Excluded past count. |
| `limitations` | `Array[String]` | Required | Limitations. |
| `policy_version` | `String` | Required | Policy version. |
| `ratio` | String | Required | This is a container for any-of cases. |
| `status` | [`Status14Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/status-14.md) | Required | Status. |
| `threshold` | `String` | Required | Threshold. |
| `total_amount` | `String` | Required | Total amount. |
| `transaction_count` | `Integer` | Required | Transaction count. |
| `window_boundary` | `String` | Required, Constant | Window boundary.<br><br>**Value**: `'left_open_right_closed'` |
| `window_end` | `String` | Required | Window end. |
| `window_hours` | `Integer` | Required | Window hours. |
| `window_start` | `String` | Required | Window start. |


# Example

```ruby
velocity_response = VelocityResponse.new(
  'True',
  false,
  'baseline_amount_per_hour6',
  BaselineProvenanceEnum::SYNTHETIC_BASELINE,
  'baseline_window_end6',
  'baseline_window_start0',
  'String1',
  'current_amount_per_hour4',
  110,
  2,
  [
    'limitations7',
    'limitations6',
    'limitations5'
  ],
  'policy_version8',
  'String1',
  Status14Enum::INSUFFICIENT_BASELINE,
  'threshold8',
  'total_amount6',
  238,
  'left_open_right_closed',
  'window_end0',
  124,
  'window_start6'
)
```



