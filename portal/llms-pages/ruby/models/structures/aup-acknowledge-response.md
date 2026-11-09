# Aup Acknowledge Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkF1cEFja25vd2xlZGdlUmVzcG9uc2U

AupAcknowledgeResponse.


# Class Name

`AupAcknowledgeResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `acknowledgement_token` | String | Required | This is a container for any-of cases. |
| `choice` | [`ChoiceEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/choice.md) | Required | Choice. |
| `compliance_decision` | `String` | Required, Constant | Compliance decision.<br><br>**Value**: `'NOT_MADE'` |
| `description_digest` | `String` | Required | Description digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `evaluation_id` | `String` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` |
| `expires_at` | String | Required | This is a container for any-of cases. |
| `external_action_authorized` | `String` | Required, Constant | External action authorized.<br><br>**Value**: `'False'` |
| `source` | `String` | Required, Constant | Source.<br><br>**Value**: `'synthetic'` |
| `warning_copy_version` | `String` | Required, Constant | Warning copy version.<br><br>**Value**: `'aup-warning-v1'` |


# Example

```ruby
aup_acknowledge_response = AupAcknowledgeResponse.new(
  'String1',
  ChoiceEnum::ACKNOWLEDGE_AND_CONTINUE,
  'NOT_MADE',
  'description_digest8',
  'evaluation_id4',
  'String7',
  'False',
  'synthetic',
  'aup-warning-v1'
)
```



