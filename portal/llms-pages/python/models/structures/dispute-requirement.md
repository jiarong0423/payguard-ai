# Dispute Requirement

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkRpc3B1dGVSZXF1aXJlbWVudA

DisputeRequirement.


# Class Name

`DisputeRequirement`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `accepted_attachment_count` | `int` | Required | Accepted attachment count.<br><br>**Constraints**: `>= 0`, `<= 20` |
| `action` | str \| None | Optional | This is a container for any-of cases. |
| `evidence_type` | str \| None | Optional | This is a container for any-of cases. |
| `mandatory` | `bool` | Required | Mandatory. |
| `proof_count` | `int` | Required | Proof count.<br><br>**Constraints**: `>= 0`, `<= 128` |
| `provider_evidence_type` | `str` | Required | Provider evidence type.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `128`, *Pattern*: `^[A-Z][A-Z0-9_]{0,127}$` |
| `request_id` | `str` | Required | Request id.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}$` |
| `requirement_state` | [`RequirementStateEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/requirement-state.md) | Required | Requirement state. |
| `source` | `str` | Required | Source.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `128`, *Pattern*: `^[A-Z][A-Z0-9_]{0,127}$` |


# Example

```python
from tradeglotlocalconsole.models.dispute_requirement import DisputeRequirement
from tradeglotlocalconsole.models.requirement_state_enum import RequirementStateEnum

dispute_requirement = DisputeRequirement(
    accepted_attachment_count=20,
    mandatory=False,
    proof_count=68,
    provider_evidence_type='provider_evidence_type6',
    request_id='request_id8',
    requirement_state=RequirementStateEnum.CONTEXT_ONLY,
    source='source6',
    action='String3',
    evidence_type='String5'
)
```



