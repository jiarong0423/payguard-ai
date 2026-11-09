# Time Evidence 1 Events

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRlRpbWVFdmlkZW5jZTFFdmVudHM


# Data Type

`MessageTimeEvent | TimeEvent`


# Cases

| Type |
|  --- |
| [`MessageTimeEvent`](http://localhost:3000/llms-pages/python/models/structures/message-time-event.md) |
| [`TimeEvent`](http://localhost:3000/llms-pages/python/models/structures/time-event.md) |


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



