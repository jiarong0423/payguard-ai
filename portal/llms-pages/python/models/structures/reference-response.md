# Reference Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRlJlZmVyZW5jZVJlc3BvbnNl

ReferenceResponse.


# Class Name

`ReferenceResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `advisory_only` | `bool` | Required | Advisory only. |
| `corpus_digest` | `str` | Required | Corpus digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `corpus_digests` | [`ReferenceDigests`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/reference-digests.md) | Required | ReferenceDigests. |
| `corpus_id` | `str` | Required, Constant | Corpus id.<br><br>**Value**: `"payguard-us-official-references-v2"` |
| `filters_applied` | [`ReferenceFilters`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/reference-filters.md) | Required | ReferenceFilters. |
| `limitations` | `List[str]` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `32`, *Minimum Length*: `1`, *Maximum Length*: `2000` |
| `operational_authority` | `str` | Required, Constant | Operational authority.<br><br>**Value**: `"REFERENCE_ONLY_NO_ACTION_AUTHORIZATION"` |
| `results` | [`List[ReferenceCitation]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/reference-citation.md) | Required | Results.<br><br>**Constraints**: *Maximum Items*: `10` |
| `schema_version` | `int` | Required | Schema version.<br><br>**Constraints**: `>= 1`, `<= 1` |
| `source` | `str` | Required, Constant | Source.<br><br>**Value**: `"public_reference"` |
| `status` | [`Status13Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/status-13.md) | Required | Status. |


# Example

```python
from tradeglotlocalconsole.models.case_outcome_enum import CaseOutcomeEnum
from tradeglotlocalconsole.models.case_stage_2_enum import CaseStage2Enum
from tradeglotlocalconsole.models.case_stage_enum import CaseStageEnum
from tradeglotlocalconsole.models.decision_date_status_enum import DecisionDateStatusEnum
from tradeglotlocalconsole.models.effective_date_status_enum import EffectiveDateStatusEnum
from tradeglotlocalconsole.models.material_type_1_enum import MaterialType1Enum
from tradeglotlocalconsole.models.material_type_4_enum import MaterialType4Enum
from tradeglotlocalconsole.models.reference_citation import ReferenceCitation
from tradeglotlocalconsole.models.reference_digests import ReferenceDigests
from tradeglotlocalconsole.models.reference_filters import ReferenceFilters
from tradeglotlocalconsole.models.reference_response import ReferenceResponse
from tradeglotlocalconsole.models.source_updated_date_status_enum import SourceUpdatedDateStatusEnum
from tradeglotlocalconsole.models.status_13_enum import Status13Enum
from tradeglotlocalconsole.models.theme_enum import ThemeEnum

reference_response = ReferenceResponse(
    advisory_only=False,
    corpus_digest='corpus_digest4',
    corpus_digests=ReferenceDigests(
        chunks_sha_256='chunks_sha2564',
        sources_sha_256='sources_sha2562'
    ),
    filters_applied=ReferenceFilters(
        as_of='String1',
        case_stage=CaseStage2Enum.PROCEDURAL_ORDER,
        limit=10,
        material_types=[
            MaterialType4Enum.OFFICIAL_POLICY,
            MaterialType4Enum.PUBLIC_COURT_ORDER_COPY
        ],
        max_source_age_days=28,
        require_known_source_date=False,
        theme=ThemeEnum.DISPUTE_MEDIATION
    ),
    limitations=[
        'limitations3',
        'limitations4',
        'limitations5'
    ],
    results=[
        ReferenceCitation(
            case_outcome=CaseOutcomeEnum.SETTLEMENT_APPROVAL_NOT_FINAL_MERITS,
            case_stage=CaseStageEnum.PROCEDURAL_ORDER,
            chunk_id='chunk_id2',
            decision_acceptance_deadline='String5',
            decision_date='String9',
            decision_date_status=DecisionDateStatusEnum.NOT_APPLICABLE,
            effective_date='String5',
            effective_date_status=EffectiveDateStatusEnum.DOCUMENT_STATED,
            jurisdiction_label='jurisdiction_label4',
            locator='locator8',
            material_type=MaterialType1Enum.OFFICIAL_API_REFERENCE,
            relevance_score=128,
            retrieved_at='retrieved_at0',
            source_id='source_id0',
            source_title='source_title8',
            source_updated_date='String9',
            source_updated_date_status=SourceUpdatedDateStatusEnum.DOCUMENT_STATED,
            text='text4',
            text_sha_256='text_sha2566',
            title='title8',
            url='url0'
        )
    ],
    schema_version=1,
    status=Status13Enum.REFERENCES_FOUND
)
```



