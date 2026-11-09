# Policy Assessment Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRlBvbGljeUFzc2Vzc21lbnRSZXNwb25zZQ

PolicyAssessmentResponse.


# Class Name

`PolicyAssessmentResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `advisory_only` | `bool` | Required | Advisory only. |
| `chunks` | [`List[PolicyChunk]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/policy-chunk.md) | Required | Chunks.<br><br>**Constraints**: *Maximum Items*: `29` |
| `corpus_digest` | `str` | Required | Corpus digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `corpus_digests` | [`ReferenceDigests`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/reference-digests.md) | Required | ReferenceDigests. |
| `corpus_id` | `str` | Required, Constant | Corpus id.<br><br>**Value**: `"payguard-us-official-references-v2"` |
| `coverage` | [`PolicyCoverage`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/policy-coverage.md) | Required | PolicyCoverage. |
| `current_policy_applicability` | `str` | Required, Constant | Current policy applicability.<br><br>**Value**: `"NOT_ESTABLISHED"` |
| `filters_applied` | [`PolicyContext`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/policy-context.md) | Required | PolicyContext. |
| `limitations` | `List[str]` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `32`, *Minimum Length*: `1`, *Maximum Length*: `2000` |
| `operational_authority` | `str` | Required, Constant | Operational authority.<br><br>**Value**: `"REFERENCE_ONLY_NO_ACTION_AUTHORIZATION"` |
| `reason_codes` | [`List[ReasonCode1Enum]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/reason-code-1.md) | Required | Reason codes.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `15` |
| `requires_human_review` | `bool` | Required | Requires human review. |
| `schema_version` | `int` | Required | Schema version.<br><br>**Constraints**: `>= 1`, `<= 1` |
| `source` | `str` | Required, Constant | Source.<br><br>**Value**: `"public_reference"` |
| `sources` | [`List[PolicySource]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/policy-source.md) | Required | Sources.<br><br>**Constraints**: *Maximum Items*: `16` |
| `status` | `str` | Required, Constant | Status.<br><br>**Value**: `"INCOMPLETE_POLICY_EVIDENCE"` |
| `version` | `str` | Required, Constant | Version.<br><br>**Value**: `"payguard.applicability.v1"` |


# Example

```python
from tradeglotlocalconsole.models.case_outcome_enum import CaseOutcomeEnum
from tradeglotlocalconsole.models.case_stage_enum import CaseStageEnum
from tradeglotlocalconsole.models.decision_date_status_enum import DecisionDateStatusEnum
from tradeglotlocalconsole.models.effective_date_status_enum import EffectiveDateStatusEnum
from tradeglotlocalconsole.models.material_type_1_enum import MaterialType1Enum
from tradeglotlocalconsole.models.missing_official_policy_theme_enum import MissingOfficialPolicyThemeEnum
from tradeglotlocalconsole.models.observation_status_enum import ObservationStatusEnum
from tradeglotlocalconsole.models.policy_assessment_response import PolicyAssessmentResponse
from tradeglotlocalconsole.models.policy_chunk import PolicyChunk
from tradeglotlocalconsole.models.policy_context import PolicyContext
from tradeglotlocalconsole.models.policy_coverage import PolicyCoverage
from tradeglotlocalconsole.models.policy_source import PolicySource
from tradeglotlocalconsole.models.policy_theme_counts import PolicyThemeCounts
from tradeglotlocalconsole.models.reason_code_1_enum import ReasonCode1Enum
from tradeglotlocalconsole.models.reference_digests import ReferenceDigests
from tradeglotlocalconsole.models.source_updated_date_status_enum import SourceUpdatedDateStatusEnum
from tradeglotlocalconsole.models.theme_enum import ThemeEnum

policy_assessment_response = PolicyAssessmentResponse(
    advisory_only=False,
    chunks=[
        PolicyChunk(
            case_outcome=CaseOutcomeEnum.SETTLEMENT_APPROVAL_NOT_FINAL_MERITS,
            case_stage=CaseStageEnum.PROCEDURAL_ORDER,
            chunk_id='chunk_id6',
            material_type=MaterialType1Enum.OFFICIAL_POLICY,
            source_id='source_id6',
            text_sha_256='text_sha2560',
            theme=ThemeEnum.VELOCITY_GUARD
        )
    ],
    corpus_digest='corpus_digest2',
    corpus_digests=ReferenceDigests(
        chunks_sha_256='chunks_sha2564',
        sources_sha_256='sources_sha2562'
    ),
    coverage=PolicyCoverage(
        complete=False,
        missing_official_policy_themes=[
            MissingOfficialPolicyThemeEnum.SOURCE_COMPLIANCE
        ],
        official_policy_chunk_count_by_theme=PolicyThemeCounts(
            dispute_mediation=12,
            source_compliance=29,
            velocity_guard=29
        ),
        official_policy_source_ids=[
            'official_policy_source_ids0'
        ],
        regional_source_count=16,
        selected_chunk_count=29,
        selected_source_count=16
    ),
    filters_applied=PolicyContext(
        as_of='as_of0',
        observation_max_age_days=28,
        theme=ThemeEnum.DISPUTE_MEDIATION
    ),
    limitations=[
        'limitations5',
        'limitations6',
        'limitations7'
    ],
    reason_codes=[
        ReasonCode1Enum.NO_REFERENCE_COVERAGE,
        ReasonCode1Enum.SUMMARY_COVERAGE_INCOMPLETE,
        ReasonCode1Enum.CURRENT_POLICY_APPLICABILITY_NOT_ESTABLISHED
    ],
    requires_human_review=False,
    schema_version=1,
    sources=[
        PolicySource(
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
                ReasonCode1Enum.CURRENT_POLICY_APPLICABILITY_NOT_ESTABLISHED,
                ReasonCode1Enum.FUTURE_OBSERVATION
            ],
            retrieved_at='retrieved_at0',
            source_id='source_id0',
            source_updated_date='String9',
            source_updated_date_status=SourceUpdatedDateStatusEnum.DOCUMENT_STATED,
            title='title2',
            url='url0'
        )
    ]
)
```



