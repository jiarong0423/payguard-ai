# Ai Brief Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkFpQnJpZWZSZXNwb25zZQ

AiBriefResponse.


# Class Name

`AiBriefResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `advisory_only` | `str` | Required, Constant | Advisory only.<br><br>**Value**: `"True"` |
| `ai_generated` | `str` | Required, Constant | Ai generated.<br><br>**Value**: `"True"` |
| `brief` | [`GeneratedBrief`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/generated-brief.md) | Required | GeneratedBrief. |
| `compliance_decision` | `str` | Required, Constant | Compliance decision.<br><br>**Value**: `"NOT_MADE"` |
| `context_digest` | `str` | Required | Context digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `corpus_digest` | `str` | Required | Corpus digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `current_policy_applicability` | `str` | Required, Constant | Current policy applicability.<br><br>**Value**: `"NOT_ESTABLISHED"` |
| `execution_evidence` | [`ExecutionEvidenceEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/execution-evidence.md) | Required | Execution evidence. |
| `external_action_authorized` | `str` | Required, Constant | External action authorized.<br><br>**Value**: `"False"` |
| `fixture_id` | [`FixtureIdEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/fixture-id.md) | Required | Fixture id. |
| `human_review_required` | `str` | Required, Constant | Human review required.<br><br>**Value**: `"True"` |
| `limitations` | `List[str]` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `3`, *Maximum Items*: `3` |
| `model` | [`ModelEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/model.md) | Required | Model. |
| `prompt_contract_digest` | `str` | Required | Prompt contract digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `prompt_contract_id` | `str` | Required, Constant | Prompt contract id.<br><br>**Value**: `"payguard-bounded-advisory-v3"` |
| `schema_version` | `str` | Required, Constant | Schema version.<br><br>**Value**: `"1.0"` |
| `semantic_entailment` | `str` | Required, Constant | Semantic entailment.<br><br>**Value**: `"NOT_EVALUATED"` |
| `stage` | [`StageEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/stage.md) | Required | Stage. |
| `status` | `str` | Required, Constant | Status.<br><br>**Value**: `"completed"` |
| `workflow_transition_authorized` | `str` | Required, Constant | Workflow transition authorized.<br><br>**Value**: `"False"` |


# Example

```python
from tradeglotlocalconsole.models.ai_brief_response import AiBriefResponse
from tradeglotlocalconsole.models.execution_evidence_enum import ExecutionEvidenceEnum
from tradeglotlocalconsole.models.fixture_id_enum import FixtureIdEnum
from tradeglotlocalconsole.models.generated_brief import GeneratedBrief
from tradeglotlocalconsole.models.model_enum import ModelEnum
from tradeglotlocalconsole.models.stage_enum import StageEnum

ai_brief_response = AiBriefResponse(
    brief=GeneratedBrief(
        citation_ids=[
            'citation_ids5',
            'citation_ids6',
            'citation_ids7'
        ],
        evidence_points=[
            'evidence_points6',
            'evidence_points7'
        ],
        missing_evidence=[
            'missing_evidence9'
        ],
        summary='summary6'
    ),
    context_digest='context_digest6',
    corpus_digest='corpus_digest2',
    execution_evidence=ExecutionEvidenceEnum.OPERATOR_LIVE_RESPONSE,
    fixture_id=FixtureIdEnum.PAYGUARDFIXEDSYNTHETICBRIEFV1,
    limitations=[
        'limitations5'
    ],
    model=ModelEnum.ENUM_GEMINI38FLASH,
    prompt_contract_digest='prompt_contract_digest2',
    stage=StageEnum.DISPUTE_MEDIATION
)
```



