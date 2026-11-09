# Advisory Evaluation Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkFkdmlzb3J5RXZhbHVhdGlvblJlc3BvbnNl

AdvisoryEvaluationResponse.


# Class Name

`AdvisoryEvaluationResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `pii_quality` | `str` | Required, Constant | PII quality.<br><br>**Value**: `"NOT_EVALUATED"` |
| `advisory_only` | `bool` | Required | Advisory only. |
| `claim_count` | `int` | Required | Claim count.<br><br>**Constraints**: `>= 1`, `<= 20` |
| `claim_gates` | [`List[AdvisoryClaimGate]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/advisory-claim-gate.md) | Required | Claim gates.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `20` |
| `corpus_digest` | `str` | Required | Corpus digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `corpus_digests` | [`ReferenceDigests`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/reference-digests.md) | Required | ReferenceDigests. |
| `corpus_id` | `str` | Required, Constant | Corpus id.<br><br>**Value**: `"payguard-us-official-references-v2"` |
| `coverage` | [`PolicyCoverage`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/policy-coverage.md) | Required | PolicyCoverage. |
| `current_policy_applicability` | `str` | Required, Constant | Current policy applicability.<br><br>**Value**: `"NOT_ESTABLISHED"` |
| `limitations` | `List[str]` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `32`, *Minimum Length*: `1`, *Maximum Length*: `2000` |
| `model_generation` | `str` | Required, Constant | Model generation.<br><br>**Value**: `"NOT_RUN"` |
| `natural_language_action_assurance_quality` | `str` | Required, Constant | Natural language action assurance quality.<br><br>**Value**: `"NOT_EVALUATED"` |
| `operational_authority` | `str` | Required, Constant | Operational authority.<br><br>**Value**: `"REFERENCE_ONLY_NO_ACTION_AUTHORIZATION"` |
| `prompt_injection_quality` | `str` | Required, Constant | Prompt injection quality.<br><br>**Value**: `"NOT_EVALUATED"` |
| `requested_context` | [`PolicyContext`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/policy-context.md) | Required | PolicyContext. |
| `requires_human_review` | `bool` | Required | Requires human review. |
| `schema_version` | `int` | Required | Schema version.<br><br>**Constraints**: `>= 1`, `<= 1` |
| `semantic_entailment` | `str` | Required, Constant | Semantic entailment.<br><br>**Value**: `"NOT_EVALUATED"` |
| `source` | `str` | Required, Constant | Source.<br><br>**Value**: `"offline_structured_gate"` |
| `status` | [`StatusEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/status.md) | Required | Status. |
| `version` | `str` | Required, Constant | Version.<br><br>**Value**: `"payguard.advisory_eval.v1"` |


# Example

```python
from tradeglotlocalconsole.models.advisory_claim_gate import AdvisoryClaimGate
from tradeglotlocalconsole.models.advisory_evaluation_response import AdvisoryEvaluationResponse
from tradeglotlocalconsole.models.claim_type_enum import ClaimTypeEnum
from tradeglotlocalconsole.models.missing_official_policy_theme_enum import MissingOfficialPolicyThemeEnum
from tradeglotlocalconsole.models.policy_context import PolicyContext
from tradeglotlocalconsole.models.policy_coverage import PolicyCoverage
from tradeglotlocalconsole.models.policy_theme_counts import PolicyThemeCounts
from tradeglotlocalconsole.models.reason_code_enum import ReasonCodeEnum
from tradeglotlocalconsole.models.reference_digests import ReferenceDigests
from tradeglotlocalconsole.models.status_enum import StatusEnum
from tradeglotlocalconsole.models.theme_enum import ThemeEnum

advisory_evaluation_response = AdvisoryEvaluationResponse(
    advisory_only=False,
    claim_count=20,
    claim_gates=[
        AdvisoryClaimGate(
            claim_index=19,
            claim_type=ClaimTypeEnum.POLICY_REFERENCE,
            reason_codes=[
                ReasonCodeEnum.ASSURANCE_CLAIM_FORBIDDEN,
                ReasonCodeEnum.CITATION_UNKNOWN,
                ReasonCodeEnum.CITATION_REGION_MISMATCH
            ],
            status=StatusEnum.INCOMPLETE_EVIDENCE,
            trusted_citation_chunk_ids=[
                'trusted_citation_chunk_ids4',
                'trusted_citation_chunk_ids5'
            ]
        )
    ],
    corpus_digest='corpus_digest4',
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
    limitations=[
        'limitations3',
        'limitations4',
        'limitations5'
    ],
    requested_context=PolicyContext(
        as_of='as_of8',
        observation_max_age_days=14,
        theme=ThemeEnum.DISPUTE_MEDIATION
    ),
    requires_human_review=False,
    schema_version=1,
    status=StatusEnum.INCOMPLETE_EVIDENCE
)
```



