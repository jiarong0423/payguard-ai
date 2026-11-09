# Event

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkV2ZW50


# Class Name

`Event`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `at` | `String` | Optional | At.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `40` |
| `channel` | [`ChannelEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/channel.md) | Optional | Channel. |
| `direction` | [`DirectionEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/direction.md) | Optional | Direction. |
| `kind` | [`Kind1Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/kind-1.md) | Optional | Kind. |
| `message_digest` | `String` | Optional | Message digest.<br><br>**Constraints**: *Pattern*: `^[0-9a-f]{64}$` |
| `source` | [`Source6Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/source-6.md) | Optional | Source. |
| `topic` | [`TopicEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/topic.md) | Optional | Topic. |


# Example

```ruby
event = Event.new(
  'at6',
  ChannelEnum::EMAIL,
  DirectionEnum::INBOUND,
  Kind1Enum::MESSAGE,
  'message_digest6',
  envrr,
  envrr
)
```



