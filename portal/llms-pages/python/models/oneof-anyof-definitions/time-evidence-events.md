# Time Evidence Events

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRlRpbWVFdmlkZW5jZUV2ZW50cw


# Data Type

`MessageTimeEvent | TimeEvent`


# Cases

| Type |
|  --- |
| [`MessageTimeEvent`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/message-time-event.md) |
| [`TimeEvent`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/time-event.md) |


# MessageTimeEvent

## Initialization Code

### Example

```python
value = MessageTimeEvent(
    at='at4',
    channel=ChannelEnum.EMAIL,
    direction=DirectionEnum.INBOUND,
    message_digest='message_digest2',
    topic=TopicEnum.ORDER_DETAILS_PROVIDED
)
```


# TimeEvent

## Initialization Code

### Example

```python
value = TimeEvent(
    at='at2',
    kind=KindEnum.DELIVERY,
    source=Source5Enum.PROVIDER
)
```



