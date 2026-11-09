# Dispute Requirement

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkRpc3B1dGVSZXF1aXJlbWVudA

DisputeRequirement.


# Class Name

`DisputeRequirement`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `accepted_attachment_count` | `Integer` | Required | Accepted attachment count.<br><br>**Constraints**: `>= 0`, `<= 20` |
| `action` | String \| nil | Optional | This is a container for any-of cases. |
| `evidence_type` | String \| nil | Optional | This is a container for any-of cases. |
| `mandatory` | `TrueClass \| FalseClass` | Required | Mandatory. |
| `proof_count` | `Integer` | Required | Proof count.<br><br>**Constraints**: `>= 0`, `<= 128` |
| `provider_evidence_type` | `String` | Required | Provider evidence type.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `128`, *Pattern*: `^[A-Z][A-Z0-9_]{0,127}$` |
| `request_id` | `String` | Required | Request id.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}$` |
| `requirement_state` | [`RequirementStateEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/requirement-state.md) | Required | Requirement state. |
| `source` | `String` | Required | Source.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `128`, *Pattern*: `^[A-Z][A-Z0-9_]{0,127}$` |


# Example

```ruby
dispute_requirement = DisputeRequirement.new(
  20,
  false,
  68,
  'provider_evidence_type6',
  'request_id8',
  RequirementStateEnum::CONTEXT_ONLY,
  'source6',
  'String3',
  'String5'
)
```



