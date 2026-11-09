# Reference Citation

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRlJlZmVyZW5jZUNpdGF0aW9u

ReferenceCitation.


# Class Name

`ReferenceCitation`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `case_outcome` | [CaseOutcome](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/case-outcome.md) | Required | This is a container for any-of cases. |
| `case_stage` | [`CaseStageEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/case-stage.md) | Required | Case stage. |
| `chunk_id` | `str` | Required | Chunk id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `decision_acceptance_deadline` | str | Required | This is a container for any-of cases. |
| `decision_date` | str | Required | This is a container for any-of cases. |
| `decision_date_status` | [`DecisionDateStatusEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/decision-date-status.md) | Required | Decision date status. |
| `effective_date` | str | Required | This is a container for any-of cases. |
| `effective_date_status` | [`EffectiveDateStatusEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/effective-date-status.md) | Required | Effective date status. |
| `jurisdiction` | `str` | Required, Constant | Jurisdiction.<br><br>**Value**: `"US"` |
| `jurisdiction_label` | `str` | Required | Jurisdiction label.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` |
| `locator` | `str` | Required | Locator.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `8000` |
| `material_type` | [`MaterialType1Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/material-type-1.md) | Required | Material type. |
| `relevance_score` | `int` | Required | Relevance score.<br><br>**Constraints**: `>= 1`, `<= 128` |
| `retrieved_at` | `str` | Required | Retrieved at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` |
| `source_id` | `str` | Required | Source id.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `128` |
| `source_title` | `str` | Required | Source title.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `8000` |
| `source_updated_date` | str | Required | This is a container for any-of cases. |
| `source_updated_date_status` | [`SourceUpdatedDateStatusEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/source-updated-date-status.md) | Required | Source updated date status. |
| `text` | `str` | Required | Text.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `8000` |
| `text_sha_256` | `str` | Required | Text sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `title` | `str` | Required | Title.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `8000` |
| `url` | `str` | Required | Url.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` |


# Example

```python
from tradeglotlocalconsole.models.case_outcome_enum import CaseOutcomeEnum
from tradeglotlocalconsole.models.case_stage_enum import CaseStageEnum
from tradeglotlocalconsole.models.decision_date_status_enum import DecisionDateStatusEnum
from tradeglotlocalconsole.models.effective_date_status_enum import EffectiveDateStatusEnum
from tradeglotlocalconsole.models.material_type_1_enum import MaterialType1Enum
from tradeglotlocalconsole.models.reference_citation import ReferenceCitation
from tradeglotlocalconsole.models.source_updated_date_status_enum import SourceUpdatedDateStatusEnum

reference_citation = ReferenceCitation(
    case_outcome=CaseOutcomeEnum.SETTLEMENT_APPROVAL_NOT_FINAL_MERITS,
    case_stage=CaseStageEnum.PROCEDURAL_ORDER,
    chunk_id='chunk_id6',
    decision_acceptance_deadline='String3',
    decision_date='String7',
    decision_date_status=DecisionDateStatusEnum.NOT_APPLICABLE,
    effective_date='String7',
    effective_date_status=EffectiveDateStatusEnum.DOCUMENT_STATED,
    jurisdiction_label='jurisdiction_label2',
    locator='locator6',
    material_type=MaterialType1Enum.OFFICIAL_API_REFERENCE,
    relevance_score=128,
    retrieved_at='retrieved_at8',
    source_id='source_id8',
    source_title='source_title0',
    source_updated_date='String7',
    source_updated_date_status=SourceUpdatedDateStatusEnum.DOCUMENT_STATED,
    text='text6',
    text_sha_256='text_sha2568',
    title='title0',
    url='url8'
)
```



