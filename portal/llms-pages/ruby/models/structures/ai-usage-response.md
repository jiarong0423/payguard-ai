# Ai Usage Response

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRkFpVXNhZ2VSZXNwb25zZQ

AiUsageResponse.


# Class Name

`AiUsageResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `content_logged` | `TrueClass \| FalseClass` | Optional | Content logged.<br><br>**Default**: `false` |
| `cost_note` | `String` | Required | Cost note. |
| `entries` | [`Array[AiUsageEntry]`](http://localhost:3000/llms-pages/ruby/models/structures/ai-usage-entry.md) | Required | Entries.<br><br>**Constraints**: *Maximum Items*: `50` |
| `price_table_source` | `String` | Required | Price table source. |
| `source` | [`Source1Enum`](http://localhost:3000/llms-pages/ruby/models/enumerations/source-1.md) | Required | Source. |


# Example

```ruby
ai_usage_response = AiUsageResponse.new(
  'cost_note2',
  [
    AiUsageEntry.new(
      'at6',
      254,
      OutcomeEnum::OK,
      Stage2Enum::STUDIO_AGENT,
      'String7',
      'String9',
      196,
      54,
      118
    )
  ],
  'price_table_source8',
  Source1Enum::SESSION_MEMORY,
  false
)
```



