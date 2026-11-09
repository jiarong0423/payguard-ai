# Policy Assessment Response

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRlBvbGljeUFzc2Vzc21lbnRSZXNwb25zZQ

PolicyAssessmentResponse.


# Class Name

`PolicyAssessmentResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `advisory_only` | `TrueClass \| FalseClass` | Required | Advisory only. |
| `chunks` | [`Array[PolicyChunk]`](http://localhost:3000/llms-pages/ruby/models/structures/policy-chunk.md) | Required | Chunks.<br><br>**Constraints**: *Maximum Items*: `29` |
| `corpus_digest` | `String` | Required | Corpus digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `corpus_digests` | [`ReferenceDigests`](http://localhost:3000/llms-pages/ruby/models/structures/reference-digests.md) | Required | ReferenceDigests. |
| `corpus_id` | `String` | Required, Constant | Corpus id.<br><br>**Value**: `'payguard-us-official-references-v2'` |
| `coverage` | [`PolicyCoverage`](http://localhost:3000/llms-pages/ruby/models/structures/policy-coverage.md) | Required | PolicyCoverage. |
| `current_policy_applicability` | `String` | Required, Constant | Current policy applicability.<br><br>**Value**: `'NOT_ESTABLISHED'` |
| `filters_applied` | [`PolicyContext`](http://localhost:3000/llms-pages/ruby/models/structures/policy-context.md) | Required | PolicyContext. |
| `limitations` | `Array[String]` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `32`, *Minimum Length*: `1`, *Maximum Length*: `2000` |
| `operational_authority` | `String` | Required, Constant | Operational authority.<br><br>**Value**: `'REFERENCE_ONLY_NO_ACTION_AUTHORIZATION'` |
| `reason_codes` | [`Array[ReasonCode1Enum]`](http://localhost:3000/llms-pages/ruby/models/enumerations/reason-code-1.md) | Required | Reason codes.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `15` |
| `requires_human_review` | `TrueClass \| FalseClass` | Required | Requires human review. |
| `schema_version` | `Integer` | Required | Schema version.<br><br>**Constraints**: `>= 1`, `<= 1` |
| `source` | `String` | Required, Constant | Source.<br><br>**Value**: `'public_reference'` |
| `sources` | [`Array[PolicySource]`](http://localhost:3000/llms-pages/ruby/models/structures/policy-source.md) | Required | Sources.<br><br>**Constraints**: *Maximum Items*: `16` |
| `status` | `String` | Required, Constant | Status.<br><br>**Value**: `'INCOMPLETE_POLICY_EVIDENCE'` |
| `version` | `String` | Required, Constant | Version.<br><br>**Value**: `'payguard.applicability.v1'` |


# Example

```ruby
policy_assessment_response = PolicyAssessmentResponse.new(
  false,
  [
    PolicyChunk.new(
      CaseOutcomeEnum::SETTLEMENT_APPROVAL_NOT_FINAL_MERITS,
      CaseStageEnum::PROCEDURAL_ORDER,
      'chunk_id6',
      'US',
      MaterialType1Enum::OFFICIAL_POLICY,
      'source_id6',
      'text_sha2560',
      ThemeEnum::VELOCITY_GUARD
    )
  ],
  'corpus_digest2',
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
  PolicyContext.new(
    'as_of0',
    'US',
    28,
    ThemeEnum::DISPUTE_MEDIATION
  ),
  [
    'limitations5',
    'limitations6',
    'limitations7'
  ],
  'REFERENCE_ONLY_NO_ACTION_AUTHORIZATION',
  [
    ReasonCode1Enum::NO_REFERENCE_COVERAGE,
    ReasonCode1Enum::SUMMARY_COVERAGE_INCOMPLETE,
    ReasonCode1Enum::CURRENT_POLICY_APPLICABILITY_NOT_ESTABLISHED
  ],
  false,
  1,
  'public_reference',
  [
    PolicySource.new(
      [
        'citation_chunk_ids2',
        'citation_chunk_ids3'
      ],
      'public_reference_summary',
      'NOT_ESTABLISHED',
      'String5',
      'String9',
      DecisionDateStatusEnum::DOCUMENT_STATED,
      'String7',
      EffectiveDateStatusEnum::DOCUMENT_STATED,
      'jurisdiction0',
      'US',
      MaterialType1Enum::PUBLIC_COURT_ORDER_COPY,
      'saved_retrieved_at_exact_elapsed_time',
      ObservationStatusEnum::FUTURE_OBSERVATION,
      [
        ReasonCode1Enum::CURRENT_POLICY_APPLICABILITY_NOT_ESTABLISHED,
        ReasonCode1Enum::FUTURE_OBSERVATION
      ],
      'authored_paraphrase_not_full_source',
      'retrieved_at0',
      'source_id0',
      'String9',
      SourceUpdatedDateStatusEnum::DOCUMENT_STATED,
      'title2',
      'url0'
    )
  ],
  'INCOMPLETE_POLICY_EVIDENCE',
  'payguard.applicability.v1'
)
```



