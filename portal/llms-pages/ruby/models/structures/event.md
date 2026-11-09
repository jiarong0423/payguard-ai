# Event

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRkV2ZW50


# Class Name

`Event`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `at` | `String` | Optional | At.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `40` |
| `channel` | [`ChannelEnum`](http://localhost:3000/llms-pages/ruby/models/enumerations/channel.md) | Optional | Channel. |
| `direction` | [`DirectionEnum`](http://localhost:3000/llms-pages/ruby/models/enumerations/direction.md) | Optional | Direction. |
| `kind` | [`Kind1Enum`](http://localhost:3000/llms-pages/ruby/models/enumerations/kind-1.md) | Optional | Kind. |
| `message_digest` | `String` | Optional | Message digest.<br><br>**Constraints**: *Pattern*: `^[0-9a-f]{64}$` |
| `source` | [`Source6Enum`](http://localhost:3000/llms-pages/ruby/models/enumerations/source-6.md) | Optional | Source. |
| `topic` | [`TopicEnum`](http://localhost:3000/llms-pages/ruby/models/enumerations/topic.md) | Optional | Topic. |


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



