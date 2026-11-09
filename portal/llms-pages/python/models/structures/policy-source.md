# Policy Source

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRlBvbGljeVNvdXJjZQ

PolicySource.


# Class Name

`PolicySource`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `citation_chunk_ids` | `List[str]` | Required | Citation chunk ids.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `29`, *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `content_class` | `str` | Required, Constant | Content class.<br><br>**Value**: `"public_reference_summary"` |
| `current_policy_applicability` | `str` | Required, Constant | Current policy applicability.<br><br>**Value**: `"NOT_ESTABLISHED"` |
| `decision_acceptance_deadline` | str | Required | This is a container for any-of cases. |
| `decision_date` | str | Required | This is a container for any-of cases. |
| `decision_date_status` | [`DecisionDateStatusEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/decision-date-status.md) | Required | Decision date status. |
| `effective_date` | str | Required | This is a container for any-of cases. |
| `effective_date_status` | [`EffectiveDateStatusEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/effective-date-status.md) | Required | Effective date status. |
| `jurisdiction` | `str` | Required | Jurisdiction.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` |
| `jurisdiction_normalized` | `str` | Required, Constant | Jurisdiction normalized.<br><br>**Value**: `"US"` |
| `material_type` | [`MaterialType1Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/material-type-1.md) | Required | Material type. |
| `observation_age_basis` | `str` | Required, Constant | Observation age basis.<br><br>**Value**: `"saved_retrieved_at_exact_elapsed_time"` |
| `observation_status` | [`ObservationStatusEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/observation-status.md) | Required | Observation status. |
| `reason_codes` | [`List[ReasonCode1Enum]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/reason-code-1.md) | Required | Reason codes.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `15` |
| `representation` | `str` | Required, Constant | Representation.<br><br>**Value**: `"authored_paraphrase_not_full_source"` |
| `retrieved_at` | `str` | Required | Retrieved at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` |
| `source_id` | `str` | Required | Source id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `source_updated_date` | str | Required | This is a container for any-of cases. |
| `source_updated_date_status` | [`SourceUpdatedDateStatusEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/source-updated-date-status.md) | Required | Source updated date status. |
| `title` | `str` | Required | Title.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` |
| `url` | `str` | Required | Url.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` |


# Example

```python
from tradeglotlocalconsole.models.decision_date_status_enum import DecisionDateStatusEnum
from tradeglotlocalconsole.models.effective_date_status_enum import EffectiveDateStatusEnum
from tradeglotlocalconsole.models.material_type_1_enum import MaterialType1Enum
from tradeglotlocalconsole.models.observation_status_enum import ObservationStatusEnum
from tradeglotlocalconsole.models.policy_source import PolicySource
from tradeglotlocalconsole.models.reason_code_1_enum import ReasonCode1Enum
from tradeglotlocalconsole.models.source_updated_date_status_enum import SourceUpdatedDateStatusEnum

policy_source = PolicySource(
    citation_chunk_ids=[
        'citation_chunk_ids2',
        'citation_chunk_ids3'
    ],
    decision_acceptance_deadline='String5',
    decision_date='String9',
    decision_date_status=DecisionDateStatusEnum.DOCUMENT_STATED,
    effective_date='String7',
    effective_date_status=EffectiveDateStatusEnum.DOCUMENT_STATED,
    jurisdiction='jurisdiction0',
    material_type=MaterialType1Enum.PUBLIC_COURT_ORDER_COPY,
    observation_status=ObservationStatusEnum.FUTURE_OBSERVATION,
    reason_codes=[
        ReasonCode1Enum.DOCUMENT_UPDATE_IN_FUTURE,
        ReasonCode1Enum.DOCUMENT_UPDATE_DATE_MISSING
    ],
    retrieved_at='retrieved_at0',
    source_id='source_id0',
    source_updated_date='String9',
    source_updated_date_status=SourceUpdatedDateStatusEnum.DOCUMENT_STATED,
    title='title2',
    url='url0'
)
```



