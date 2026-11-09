# Policy Chunk

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRlBvbGljeUNodW5r

PolicyChunk.


# Class Name

`PolicyChunk`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `case_outcome` | [CaseOutcome](http://localhost:3000/llms-pages/ruby/models/enumerations/case-outcome.md) | Required | This is a container for any-of cases. |
| `case_stage` | [`CaseStageEnum`](http://localhost:3000/llms-pages/ruby/models/enumerations/case-stage.md) | Required | Case stage. |
| `chunk_id` | `String` | Required | Chunk id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `jurisdiction` | `String` | Required, Constant | Jurisdiction.<br><br>**Value**: `'US'` |
| `material_type` | [`MaterialType1Enum`](http://localhost:3000/llms-pages/ruby/models/enumerations/material-type-1.md) | Required | Material type. |
| `source_id` | `String` | Required | Source id.<br><br>**Constraints**: *Pattern*: `^[A-Z0-9-]{1,128}$` |
| `text_sha_256` | `String` | Required | Text sha256.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `theme` | [`ThemeEnum`](http://localhost:3000/llms-pages/ruby/models/enumerations/theme.md) | Required | Theme. |


# Example

```ruby
policy_chunk = PolicyChunk.new(
  CaseOutcomeEnum::SETTLEMENT_APPROVAL_NOT_FINAL_MERITS,
  CaseStageEnum::PROCEDURAL_ORDER,
  'chunk_id6',
  'US',
  MaterialType1Enum::PUBLIC_COURT_ORDER_COPY,
  'source_id8',
  'text_sha2568',
  ThemeEnum::DISPUTE_MEDIATION
)
```



