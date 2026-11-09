# Time Evidence Events

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRlRpbWVFdmlkZW5jZUV2ZW50cw


# Data Type

`MessageTimeEvent|TimeEvent`


# Cases

| Type |
|  --- |
| [`MessageTimeEvent`](http://localhost:3000/llms-pages/php/models/structures/message-time-event.md) |
| [`TimeEvent`](http://localhost:3000/llms-pages/php/models/structures/time-event.md) |


# MessageTimeEvent

## Initialization Code

### Example

```php
$value = MessageTimeEventBuilder::init(
    'at4',
    ChannelEnum::EMAIL,
    DirectionEnum::INBOUND,
    'message_digest2',
    TopicEnum::ORDER_DETAILS_PROVIDED
)->build();
```


# TimeEvent

## Initialization Code

### Example

```php
$value = TimeEventBuilder::init(
    'at2',
    KindEnum::DELIVERY,
    Source5Enum::PROVIDER
)->build();
```



