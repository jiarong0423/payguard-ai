# Policy Source

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRlBvbGljeVNvdXJjZQ

PolicySource.


# Class Name

`PolicySource`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `citation_chunk_ids` | `Array[String]` | Required | Citation chunk ids.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `29`, *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `content_class` | `String` | Required, Constant | Content class.<br><br>**Value**: `'public_reference_summary'` |
| `current_policy_applicability` | `String` | Required, Constant | Current policy applicability.<br><br>**Value**: `'NOT_ESTABLISHED'` |
| `decision_acceptance_deadline` | String | Required | This is a container for any-of cases. |
| `decision_date` | String | Required | This is a container for any-of cases. |
| `decision_date_status` | [`DecisionDateStatusEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/decision-date-status.md) | Required | Decision date status. |
| `effective_date` | String | Required | This is a container for any-of cases. |
| `effective_date_status` | [`EffectiveDateStatusEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/effective-date-status.md) | Required | Effective date status. |
| `jurisdiction` | `String` | Required | Jurisdiction.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` |
| `jurisdiction_normalized` | `String` | Required, Constant | Jurisdiction normalized.<br><br>**Value**: `'US'` |
| `material_type` | [`MaterialType1Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/material-type-1.md) | Required | Material type. |
| `observation_age_basis` | `String` | Required, Constant | Observation age basis.<br><br>**Value**: `'saved_retrieved_at_exact_elapsed_time'` |
| `observation_status` | [`ObservationStatusEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/observation-status.md) | Required | Observation status. |
| `reason_codes` | [`Array[ReasonCode1Enum]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/reason-code-1.md) | Required | Reason codes.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `15` |
| `representation` | `String` | Required, Constant | Representation.<br><br>**Value**: `'authored_paraphrase_not_full_source'` |
| `retrieved_at` | `String` | Required | Retrieved at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` |
| `source_id` | `String` | Required | Source id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `source_updated_date` | String | Required | This is a container for any-of cases. |
| `source_updated_date_status` | [`SourceUpdatedDateStatusEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/source-updated-date-status.md) | Required | Source updated date status. |
| `title` | `String` | Required | Title.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` |
| `url` | `String` | Required | Url.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` |


# Example

```ruby
policy_source = PolicySource.new(
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
    ReasonCode1Enum::DOCUMENT_UPDATE_IN_FUTURE,
    ReasonCode1Enum::DOCUMENT_UPDATE_DATE_MISSING
  ],
  'authored_paraphrase_not_full_source',
  'retrieved_at0',
  'source_id0',
  'String9',
  SourceUpdatedDateStatusEnum::DOCUMENT_STATED,
  'title2',
  'url0'
)
```



