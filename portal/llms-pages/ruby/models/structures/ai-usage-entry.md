# Ai Usage Entry

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkFpVXNhZ2VFbnRyeQ

AiUsageEntry.


# Class Name

`AiUsageEntry`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `at` | `String` | Required | At. |
| `estimated_cost_usd` | String \| nil | Optional | This is a container for any-of cases. |
| `latency_ms` | `Integer` | Required | Latency ms.<br><br>**Constraints**: `>= 0`, `<= 3600000` |
| `model` | String \| nil | Optional | This is a container for any-of cases. |
| `outcome` | [`OutcomeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/outcome.md) | Required | Outcome. |
| `stage` | [`Stage2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/stage-2.md) | Required | Stage. |
| `tokens_in` | Integer \| nil | Optional | This is a container for any-of cases. |
| `tokens_out` | Integer \| nil | Optional | This is a container for any-of cases. |
| `tokens_total` | Integer \| nil | Optional | This is a container for any-of cases. |


# Example

```ruby
ai_usage_entry = AiUsageEntry.new(
  'at8',
  36,
  OutcomeEnum::OK,
  Stage2Enum::DISPUTE_MEDIATION,
  'String9',
  'String1',
  234,
  92,
  156
)
```



