# Time Evidence 1 Events

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRlRpbWVFdmlkZW5jZTFFdmVudHM


# Class Name

`TimeEvidence1Events`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`models.MessageTimeEvent`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/message-time-event.md) | models.TimeEvidence1EventsContainer.FromMessageTimeEvent(models.MessageTimeEvent messageTimeEvent) |
| [`models.TimeEvent`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/time-event.md) | models.TimeEvidence1EventsContainer.FromTimeEvent(models.TimeEvent timeEvent) |


# models.MessageTimeEvent

## Initialization Code

### Example

```go
value := models.TimeEvidence1EventsContainer.FromMessageTimeEvent(models.MessageTimeEvent{
    At:                   "at4",
    Channel:              models.ChannelEnum_EMAIL,
    Direction:            models.DirectionEnum_INBOUND,
    Kind:                 "MESSAGE",
    MessageDigest:        "message_digest2",
    Source:               "SELLER_PROVIDED_UNVERIFIED",
    Topic:                models.TopicEnum_ORDERDETAILSPROVIDED,
})
```


# models.TimeEvent

## Initialization Code

### Example

```go
value := models.TimeEvidence1EventsContainer.FromTimeEvent(models.TimeEvent{
    At:                   "at2",
    Kind:                 models.KindEnum_DELIVERY,
    Source:               models.Source5Enum_PROVIDER,
})
```



