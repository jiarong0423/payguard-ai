# Policy Chunk

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRlBvbGljeUNodW5r

PolicyChunk.


# Class Name

`PolicyChunk`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `case_outcome` | [CaseOutcome](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/case-outcome.md) | Required | This is a container for any-of cases. |
| `case_stage` | [`CaseStageEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/case-stage.md) | Required | Case stage. |
| `chunk_id` | `str` | Required | Chunk id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `jurisdiction` | `str` | Required, Constant | Jurisdiction.<br><br>**Value**: `"US"` |
| `material_type` | [`MaterialType1Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/material-type-1.md) | Required | Material type. |
| `source_id` | `str` | Required | Source id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `text_sha_256` | `str` | Required | Text sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `theme` | [`ThemeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/theme.md) | Required | Theme. |


# Example

```python
from tradeglotlocalconsole.models.case_outcome_enum import CaseOutcomeEnum
from tradeglotlocalconsole.models.case_stage_enum import CaseStageEnum
from tradeglotlocalconsole.models.material_type_1_enum import MaterialType1Enum
from tradeglotlocalconsole.models.policy_chunk import PolicyChunk
from tradeglotlocalconsole.models.theme_enum import ThemeEnum

policy_chunk = PolicyChunk(
    case_outcome=CaseOutcomeEnum.SETTLEMENT_APPROVAL_NOT_FINAL_MERITS,
    case_stage=CaseStageEnum.PROCEDURAL_ORDER,
    chunk_id='chunk_id6',
    material_type=MaterialType1Enum.PUBLIC_COURT_ORDER_COPY,
    source_id='source_id8',
    text_sha_256='text_sha2568',
    theme=ThemeEnum.DISPUTE_MEDIATION
)
```



