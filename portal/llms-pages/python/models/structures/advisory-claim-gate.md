# Advisory Claim Gate

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkFkdmlzb3J5Q2xhaW1HYXRl

AdvisoryClaimGate.


# Class Name

`AdvisoryClaimGate`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `claim_index` | `int` | Required | Claim index.<br><br>**Constraints**: `>= 0`, `<= 19` |
| `claim_type` | [`ClaimTypeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/claim-type.md) | Required | Claim type. |
| `reason_codes` | [`List[ReasonCodeEnum]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/reason-code.md) | Required | Reason codes.<br><br>**Constraints**: *Maximum Items*: `10` |
| `status` | [`StatusEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/status.md) | Required | Status. |
| `trusted_citation_chunk_ids` | `List[str]` | Required | Trusted citation chunk ids.<br><br>**Constraints**: *Maximum Items*: `10`, *Pattern*: `^[A-Z0-9-]{1,128}$` |


# Example

```python
from tradeglotlocalconsole.models.advisory_claim_gate import AdvisoryClaimGate
from tradeglotlocalconsole.models.claim_type_enum import ClaimTypeEnum
from tradeglotlocalconsole.models.reason_code_enum import ReasonCodeEnum
from tradeglotlocalconsole.models.status_enum import StatusEnum

advisory_claim_gate = AdvisoryClaimGate(
    claim_index=19,
    claim_type=ClaimTypeEnum.PROCEDURAL_REFERENCE,
    reason_codes=[
        ReasonCodeEnum.CURRENT_POLICY_NOT_ESTABLISHED
    ],
    status=StatusEnum.INCOMPLETE_EVIDENCE,
    trusted_citation_chunk_ids=[
        'trusted_citation_chunk_ids0'
    ]
)
```



