# Message Time Event

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRk1lc3NhZ2VUaW1lRXZlbnQ

MessageTimeEvent.


# Class Name

`MessageTimeEvent`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `at` | `String` | Required | At.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `40` |
| `channel` | [`ChannelEnum`](http://localhost:3000/llms-pages/ruby/models/enumerations/channel.md) | Required | Channel. |
| `direction` | [`DirectionEnum`](http://localhost:3000/llms-pages/ruby/models/enumerations/direction.md) | Required | Direction. |
| `kind` | `String` | Required, Constant | Kind.<br><br>**Value**: `'MESSAGE'` |
| `message_digest` | `String` | Required | Message digest.<br><br>**Constraints**: *Pattern*: `^[0-9a-f]{64}$` |
| `source` | `String` | Required, Constant | Source.<br><br>**Value**: `'SELLER_PROVIDED_UNVERIFIED'` |
| `topic` | [`TopicEnum`](http://localhost:3000/llms-pages/ruby/models/enumerations/topic.md) | Required | Topic. |


# Example

```ruby
message_time_event = MessageTimeEvent.new(
  'at2',
  ChannelEnum::EMAIL,
  DirectionEnum::INBOUND,
  'MESSAGE',
  'message_digest0',
  'SELLER_PROVIDED_UNVERIFIED',
  TopicEnum::ORDER_DETAILS_PROVIDED
)
```



