# Reference Citation

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRlJlZmVyZW5jZUNpdGF0aW9u

ReferenceCitation.


# Class Name

`ReferenceCitation`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `case_outcome` | [CaseOutcome](http://localhost:3000/llms-pages/ruby/models/enumerations/case-outcome.md) | Required | This is a container for any-of cases. |
| `case_stage` | [`CaseStageEnum`](http://localhost:3000/llms-pages/ruby/models/enumerations/case-stage.md) | Required | Case stage. |
| `chunk_id` | `String` | Required | Chunk id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `decision_acceptance_deadline` | String | Required | This is a container for any-of cases. |
| `decision_date` | String | Required | This is a container for any-of cases. |
| `decision_date_status` | [`DecisionDateStatusEnum`](http://localhost:3000/llms-pages/ruby/models/enumerations/decision-date-status.md) | Required | Decision date status. |
| `effective_date` | String | Required | This is a container for any-of cases. |
| `effective_date_status` | [`EffectiveDateStatusEnum`](http://localhost:3000/llms-pages/ruby/models/enumerations/effective-date-status.md) | Required | Effective date status. |
| `jurisdiction` | `String` | Required, Constant | Jurisdiction.<br><br>**Value**: `'US'` |
| `jurisdiction_label` | `String` | Required | Jurisdiction label.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` |
| `locator` | `String` | Required | Locator.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `8000` |
| `material_type` | [`MaterialType1Enum`](http://localhost:3000/llms-pages/ruby/models/enumerations/material-type-1.md) | Required | Material type. |
| `relevance_score` | `Integer` | Required | Relevance score.<br><br>**Constraints**: `>= 1`, `<= 128` |
| `retrieved_at` | `String` | Required | Retrieved at.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `64` |
| `source_id` | `String` | Required | Source id.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `128` |
| `source_title` | `String` | Required | Source title.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `8000` |
| `source_updated_date` | String | Required | This is a container for any-of cases. |
| `source_updated_date_status` | [`SourceUpdatedDateStatusEnum`](http://localhost:3000/llms-pages/ruby/models/enumerations/source-updated-date-status.md) | Required | Source updated date status. |
| `text` | `String` | Required | Text.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `8000` |
| `text_sha_256` | `String` | Required | Text sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `title` | `String` | Required | Title.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `8000` |
| `url` | `String` | Required | Url.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` |


# Example

```ruby
reference_citation = ReferenceCitation.new(
  CaseOutcomeEnum::SETTLEMENT_APPROVAL_NOT_FINAL_MERITS,
  CaseStageEnum::PROCEDURAL_ORDER,
  'chunk_id6',
  'String3',
  'String7',
  DecisionDateStatusEnum::NOT_APPLICABLE,
  'String7',
  EffectiveDateStatusEnum::DOCUMENT_STATED,
  'US',
  'jurisdiction_label2',
  'locator6',
  MaterialType1Enum::OFFICIAL_API_REFERENCE,
  128,
  'retrieved_at8',
  'source_id8',
  'source_title0',
  'String7',
  SourceUpdatedDateStatusEnum::DOCUMENT_STATED,
  'text6',
  'text_sha2568',
  'title0',
  'url8'
)
```



