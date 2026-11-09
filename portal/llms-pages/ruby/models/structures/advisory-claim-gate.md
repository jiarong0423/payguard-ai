# Advisory Claim Gate

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkFkdmlzb3J5Q2xhaW1HYXRl

AdvisoryClaimGate.


# Class Name

`AdvisoryClaimGate`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `claim_index` | `Integer` | Required | Claim index.<br><br>**Constraints**: `>= 0`, `<= 19` |
| `claim_type` | [`ClaimTypeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/claim-type.md) | Required | Claim type. |
| `reason_codes` | [`Array[ReasonCodeEnum]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/reason-code.md) | Required | Reason codes.<br><br>**Constraints**: *Maximum Items*: `10` |
| `status` | [`StatusEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/status.md) | Required | Status. |
| `trusted_citation_chunk_ids` | `Array[String]` | Required | Trusted citation chunk ids.<br><br>**Constraints**: *Maximum Items*: `10`, *Pattern*: `^[A-Z0-9-]{1,128}$` |


# Example

```ruby
advisory_claim_gate = AdvisoryClaimGate.new(
  19,
  ClaimTypeEnum::PROCEDURAL_REFERENCE,
  [
    ReasonCodeEnum::CURRENT_POLICY_NOT_ESTABLISHED
  ],
  StatusEnum::INCOMPLETE_EVIDENCE,
  [
    'trusted_citation_chunk_ids0'
  ]
)
```



