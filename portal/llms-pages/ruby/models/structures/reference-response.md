# Reference Response

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRlJlZmVyZW5jZVJlc3BvbnNl

ReferenceResponse.


# Class Name

`ReferenceResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `advisory_only` | `TrueClass \| FalseClass` | Required | Advisory only. |
| `corpus_digest` | `String` | Required | Corpus digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `corpus_digests` | [`ReferenceDigests`](http://localhost:3000/llms-pages/ruby/models/structures/reference-digests.md) | Required | ReferenceDigests. |
| `corpus_id` | `String` | Required, Constant | Corpus id.<br><br>**Value**: `'payguard-us-official-references-v2'` |
| `filters_applied` | [`ReferenceFilters`](http://localhost:3000/llms-pages/ruby/models/structures/reference-filters.md) | Required | ReferenceFilters. |
| `limitations` | `Array[String]` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `32`, *Minimum Length*: `1`, *Maximum Length*: `2000` |
| `operational_authority` | `String` | Required, Constant | Operational authority.<br><br>**Value**: `'REFERENCE_ONLY_NO_ACTION_AUTHORIZATION'` |
| `results` | [`Array[ReferenceCitation]`](http://localhost:3000/llms-pages/ruby/models/structures/reference-citation.md) | Required | Results.<br><br>**Constraints**: *Maximum Items*: `10` |
| `schema_version` | `Integer` | Required | Schema version.<br><br>**Constraints**: `>= 1`, `<= 1` |
| `source` | `String` | Required, Constant | Source.<br><br>**Value**: `'public_reference'` |
| `status` | [`Status13Enum`](http://localhost:3000/llms-pages/ruby/models/enumerations/status-13.md) | Required | Status. |


# Example

```ruby
reference_response = ReferenceResponse.new(
  false,
  'corpus_digest4',
  ReferenceDigests.new(
    'chunks_sha2564',
    'sources_sha2562'
  ),
  'payguard-us-official-references-v2',
  ReferenceFilters.new(
    'source_updated_date_utc_calendar',
    'String1',
    CaseStage2Enum::PROCEDURAL_ORDER,
    'US',
    10,
    [
      MaterialType4Enum::OFFICIAL_POLICY,
      MaterialType4Enum::PUBLIC_COURT_ORDER_COPY
    ],
    28,
    false,
    ThemeEnum::DISPUTE_MEDIATION
  ),
  [
    'limitations3',
    'limitations4',
    'limitations5'
  ],
  'REFERENCE_ONLY_NO_ACTION_AUTHORIZATION',
  [
    ReferenceCitation.new(
      CaseOutcomeEnum::SETTLEMENT_APPROVAL_NOT_FINAL_MERITS,
      CaseStageEnum::PROCEDURAL_ORDER,
      'chunk_id2',
      'String5',
      'String9',
      DecisionDateStatusEnum::NOT_APPLICABLE,
      'String5',
      EffectiveDateStatusEnum::DOCUMENT_STATED,
      'US',
      'jurisdiction_label4',
      'locator8',
      MaterialType1Enum::OFFICIAL_API_REFERENCE,
      128,
      'retrieved_at0',
      'source_id0',
      'source_title8',
      'String9',
      SourceUpdatedDateStatusEnum::DOCUMENT_STATED,
      'text4',
      'text_sha2566',
      'title8',
      'url0'
    )
  ],
  1,
  'public_reference',
  Status13Enum::REFERENCES_FOUND
)
```



