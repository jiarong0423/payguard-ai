# Advisory Evaluation Response

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRkFkdmlzb3J5RXZhbHVhdGlvblJlc3BvbnNl

AdvisoryEvaluationResponse.


# Class Name

`AdvisoryEvaluationResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `pii_quality` | `String` | Required, Constant | PII quality.<br><br>**Value**: `'NOT_EVALUATED'` |
| `advisory_only` | `TrueClass \| FalseClass` | Required | Advisory only. |
| `claim_count` | `Integer` | Required | Claim count.<br><br>**Constraints**: `>= 1`, `<= 20` |
| `claim_gates` | [`Array[AdvisoryClaimGate]`](http://localhost:3000/llms-pages/ruby/models/structures/advisory-claim-gate.md) | Required | Claim gates.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `20` |
| `corpus_digest` | `String` | Required | Corpus digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `corpus_digests` | [`ReferenceDigests`](http://localhost:3000/llms-pages/ruby/models/structures/reference-digests.md) | Required | ReferenceDigests. |
| `corpus_id` | `String` | Required, Constant | Corpus id.<br><br>**Value**: `'payguard-us-official-references-v2'` |
| `coverage` | [`PolicyCoverage`](http://localhost:3000/llms-pages/ruby/models/structures/policy-coverage.md) | Required | PolicyCoverage. |
| `current_policy_applicability` | `String` | Required, Constant | Current policy applicability.<br><br>**Value**: `'NOT_ESTABLISHED'` |
| `limitations` | `Array[String]` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `32`, *Minimum Length*: `1`, *Maximum Length*: `2000` |
| `model_generation` | `String` | Required, Constant | Model generation.<br><br>**Value**: `'NOT_RUN'` |
| `natural_language_action_assurance_quality` | `String` | Required, Constant | Natural language action assurance quality.<br><br>**Value**: `'NOT_EVALUATED'` |
| `operational_authority` | `String` | Required, Constant | Operational authority.<br><br>**Value**: `'REFERENCE_ONLY_NO_ACTION_AUTHORIZATION'` |
| `prompt_injection_quality` | `String` | Required, Constant | Prompt injection quality.<br><br>**Value**: `'NOT_EVALUATED'` |
| `requested_context` | [`PolicyContext`](http://localhost:3000/llms-pages/ruby/models/structures/policy-context.md) | Required | PolicyContext. |
| `requires_human_review` | `TrueClass \| FalseClass` | Required | Requires human review. |
| `schema_version` | `Integer` | Required | Schema version.<br><br>**Constraints**: `>= 1`, `<= 1` |
| `semantic_entailment` | `String` | Required, Constant | Semantic entailment.<br><br>**Value**: `'NOT_EVALUATED'` |
| `source` | `String` | Required, Constant | Source.<br><br>**Value**: `'offline_structured_gate'` |
| `status` | [`StatusEnum`](http://localhost:3000/llms-pages/ruby/models/enumerations/status.md) | Required | Status. |
| `version` | `String` | Required, Constant | Version.<br><br>**Value**: `'payguard.advisory_eval.v1'` |


# Example

```ruby
advisory_evaluation_response = AdvisoryEvaluationResponse.new(
  'NOT_EVALUATED',
  false,
  20,
  [
    AdvisoryClaimGate.new(
      19,
      ClaimTypeEnum::POLICY_REFERENCE,
      [
        ReasonCodeEnum::ASSURANCE_CLAIM_FORBIDDEN,
        ReasonCodeEnum::CITATION_UNKNOWN,
        ReasonCodeEnum::CITATION_REGION_MISMATCH
      ],
      StatusEnum::INCOMPLETE_EVIDENCE,
      [
        'trusted_citation_chunk_ids4',
        'trusted_citation_chunk_ids5'
      ]
    )
  ],
  'corpus_digest4',
  ReferenceDigests.new(
    'chunks_sha2564',
    'sources_sha2562'
  ),
  'payguard-us-official-references-v2',
  PolicyCoverage.new(
    'pinned_authored_summaries_only',
    false,
    [
      MissingOfficialPolicyThemeEnum::SOURCE_COMPLIANCE
    ],
    PolicyThemeCounts.new(
      12,
      29,
      29
    ),
    [
      'official_policy_source_ids0'
    ],
    16,
    29,
    16
  ),
  'NOT_ESTABLISHED',
  [
    'limitations3',
    'limitations4',
    'limitations5'
  ],
  'NOT_RUN',
  'NOT_EVALUATED',
  'REFERENCE_ONLY_NO_ACTION_AUTHORIZATION',
  'NOT_EVALUATED',
  PolicyContext.new(
    'as_of8',
    'US',
    14,
    ThemeEnum::DISPUTE_MEDIATION
  ),
  false,
  1,
  'NOT_EVALUATED',
  'offline_structured_gate',
  StatusEnum::INCOMPLETE_EVIDENCE,
  'payguard.advisory_eval.v1'
)
```



