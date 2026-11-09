# Ai Brief Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkFpQnJpZWZSZXNwb25zZQ

AiBriefResponse.


# Class Name

`AiBriefResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `advisory_only` | `String` | Required, Constant | Advisory only.<br><br>**Value**: `'True'` |
| `ai_generated` | `String` | Required, Constant | Ai generated.<br><br>**Value**: `'True'` |
| `brief` | [`GeneratedBrief`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/generated-brief.md) | Required | GeneratedBrief. |
| `compliance_decision` | `String` | Required, Constant | Compliance decision.<br><br>**Value**: `'NOT_MADE'` |
| `context_digest` | `String` | Required | Context digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `corpus_digest` | `String` | Required | Corpus digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `current_policy_applicability` | `String` | Required, Constant | Current policy applicability.<br><br>**Value**: `'NOT_ESTABLISHED'` |
| `execution_evidence` | [`ExecutionEvidenceEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/execution-evidence.md) | Required | Execution evidence. |
| `external_action_authorized` | `String` | Required, Constant | External action authorized.<br><br>**Value**: `'False'` |
| `fixture_id` | [`FixtureIdEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/fixture-id.md) | Required | Fixture id. |
| `human_review_required` | `String` | Required, Constant | Human review required.<br><br>**Value**: `'True'` |
| `limitations` | `Array[String]` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `3`, *Maximum Items*: `3` |
| `model` | [`ModelEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/model.md) | Required | Model. |
| `prompt_contract_digest` | `String` | Required | Prompt contract digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `prompt_contract_id` | `String` | Required, Constant | Prompt contract id.<br><br>**Value**: `'payguard-bounded-advisory-v3'` |
| `schema_version` | `String` | Required, Constant | Schema version.<br><br>**Value**: `'1.0'` |
| `semantic_entailment` | `String` | Required, Constant | Semantic entailment.<br><br>**Value**: `'NOT_EVALUATED'` |
| `stage` | [`StageEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/stage.md) | Required | Stage. |
| `status` | `String` | Required, Constant | Status.<br><br>**Value**: `'completed'` |
| `workflow_transition_authorized` | `String` | Required, Constant | Workflow transition authorized.<br><br>**Value**: `'False'` |


# Example

```ruby
ai_brief_response = AiBriefResponse.new(
  'True',
  'True',
  GeneratedBrief.new(
    [
      'citation_ids5',
      'citation_ids6',
      'citation_ids7'
    ],
    [
      'evidence_points6',
      'evidence_points7'
    ],
    [
      'missing_evidence9'
    ],
    'summary6'
  ),
  'NOT_MADE',
  'context_digest6',
  'corpus_digest2',
  'NOT_ESTABLISHED',
  ExecutionEvidenceEnum::OPERATOR_LIVE_RESPONSE,
  'False',
  FixtureIdEnum::PAYGUARDFIXEDSYNTHETICBRIEFV1,
  'True',
  [
    'limitations5'
  ],
  ModelEnum::ENUM_GEMINI38FLASH,
  'prompt_contract_digest2',
  'payguard-bounded-advisory-v3',
  '1.0',
  'NOT_EVALUATED',
  StageEnum::DISPUTE_MEDIATION,
  'completed',
  'False'
)
```



