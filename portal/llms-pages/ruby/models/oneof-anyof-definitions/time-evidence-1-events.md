# Time Evidence 1 Events

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRlRpbWVFdmlkZW5jZTFFdmVudHM


# Data Type

`MessageTimeEvent | TimeEvent`


# Cases

| Type |
|  --- |
| [`MessageTimeEvent`](http://localhost:3000/llms-pages/ruby/models/structures/message-time-event.md) |
| [`TimeEvent`](http://localhost:3000/llms-pages/ruby/models/structures/time-event.md) |


# MessageTimeEvent

## Initialization Code

### Example

```ruby
value = MessageTimeEvent.new(
  'at4',
  ChannelEnum::EMAIL,
  DirectionEnum::INBOUND,
  'MESSAGE',
  'message_digest2',
  'SELLER_PROVIDED_UNVERIFIED',
  TopicEnum::ORDER_DETAILS_PROVIDED
)
```


# TimeEvent

## Initialization Code

### Example

```ruby
value = TimeEvent.new(
  'at2',
  KindEnum::DELIVERY,
  Source5Enum::PROVIDER
)
```



