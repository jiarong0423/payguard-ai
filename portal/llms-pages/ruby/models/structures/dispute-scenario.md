# Dispute Scenario

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRkRpc3B1dGVTY2VuYXJpbw

DisputeScenario.


# Class Name

`DisputeScenario`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `citations` | [`Array[ScenarioCitation]`](http://localhost:3000/llms-pages/ruby/models/structures/scenario-citation.md) | Required | Citations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `20` |
| `evidence_class` | `String` | Required, Constant | Evidence class.<br><br>**Value**: `'SYNTHETIC_DEMO_SCENARIO'` |
| `expected_route` | `String` | Required, Constant | Expected route.<br><br>**Value**: `'PREPARE_REDACTED_DRAFT_FOR_HUMAN_REVIEW'` |
| `final_authority` | `String` | Required, Constant | Final authority.<br><br>**Value**: `'PAYPAL_OR_EXTERNAL_ISSUER'` |
| `jurisdiction` | `String` | Required, Constant | Jurisdiction.<br><br>**Value**: `'US'` |
| `limitations` | `Array[String]` | Required | Limitations.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `8` |
| `scenario_id` | `String` | Required, Constant | Scenario id.<br><br>**Value**: `'US-DEMO-DISPUTE-EVIDENCE'` |
| `theme` | `String` | Required, Constant | Theme.<br><br>**Value**: `'dispute_mediation'` |
| `title` | `String` | Required, Constant | Title.<br><br>**Value**: `'INR or counterfeit evidence organization'` |


# Example

```ruby
dispute_scenario = DisputeScenario.new(
  [
    ScenarioCitation.new(
      'chunk_id0',
      'US',
      'locator0',
      MaterialTypeEnum::OFFICIAL_API_REFERENCE,
      'source_id2',
      'text_sha2564',
      'title4',
      'url2'
    )
  ],
  'SYNTHETIC_DEMO_SCENARIO',
  'PREPARE_REDACTED_DRAFT_FOR_HUMAN_REVIEW',
  'PAYPAL_OR_EXTERNAL_ISSUER',
  'US',
  [
    'limitations3'
  ],
  'US-DEMO-DISPUTE-EVIDENCE',
  'dispute_mediation',
  'INR or counterfeit evidence organization'
)
```



