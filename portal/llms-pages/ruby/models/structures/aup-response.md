# Aup Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkF1cFJlc3BvbnNl

AupResponse.


# Class Name

`AupResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `advisory_only` | `String` | Required, Constant | Advisory only.<br><br>**Value**: `'True'` |
| `compliance_decision` | `String` | Required, Constant | Compliance decision.<br><br>**Value**: `'NOT_MADE'` |
| `current_policy_applicability` | `String` | Required, Constant | Current policy applicability.<br><br>**Value**: `'NOT_ESTABLISHED'` |
| `description_digest` | `String` | Required | Description digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `evaluated_at` | `String` | Required | Evaluated at. |
| `evaluation_id` | `String` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` |
| `expires_at` | `String` | Required | Expires at. |
| `findings` | [`Array[Finding]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/finding.md) | Required | Findings. |
| `match_status` | [`MatchStatusEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/match-status.md) | Required | Match status. |
| `policy_url` | `String` | Required, Constant | Policy url.<br><br>**Value**: `'https://www.paypal.com/us/legalhub/paypal/acceptableuse-full'` |
| `policy_version` | `String` | Required | Policy version.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `128` |
| `recommendation` | `String` | Required | Recommendation.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `1000` |
| `source` | `String` | Required, Constant | Source.<br><br>**Value**: `'synthetic'` |
| `warning_copy_version` | `String` | Required, Constant | Warning copy version.<br><br>**Value**: `'aup-warning-v1'` |


# Example

```ruby
aup_response = AupResponse.new(
  'True',
  'NOT_MADE',
  'NOT_ESTABLISHED',
  'description_digest0',
  'evaluated_at6',
  'evaluation_id6',
  'expires_at4',
  [
    Finding.new(
      CategoryEnum::WEAPONS,
      'keyword_requires_policy_review'
    )
  ],
  MatchStatusEnum::NO_MATCH,
  'https://www.paypal.com/us/legalhub/paypal/acceptableuse-full',
  'policy_version0',
  'recommendation2',
  'synthetic',
  'aup-warning-v1'
)
```



