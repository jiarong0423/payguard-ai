# Time Evidence Events

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRlRpbWVFdmlkZW5jZUV2ZW50cw


# Class Name

`TimeEvidenceEvents`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`MessageTimeEvent`](http://localhost:3000/llms-pages/net-standard-library/models/structures/message-time-event.md) | TimeEvidenceEvents.FromMessageTimeEvent(MessageTimeEvent messageTimeEvent) |
| [`TimeEvent`](http://localhost:3000/llms-pages/net-standard-library/models/structures/time-event.md) | TimeEvidenceEvents.FromTimeEvent(TimeEvent timeEvent) |


# MessageTimeEvent

## Initialization Code

### Example

```csharp
TimeEvidenceEvents value = TimeEvidenceEvents.FromMessageTimeEvent(
    new MessageTimeEvent
    {
        At = "at4",
        Channel = ChannelEnum.EMAIL,
        Direction = DirectionEnum.INBOUND,
        Kind = "MESSAGE",
        MessageDigest = "message_digest2",
        Source = "SELLER_PROVIDED_UNVERIFIED",
        Topic = TopicEnum.ORDERDETAILSPROVIDED,
    }
);
```


# TimeEvent

## Initialization Code

### Example

```csharp
TimeEvidenceEvents value = TimeEvidenceEvents.FromTimeEvent(
    new TimeEvent
    {
        At = "at2",
        Kind = KindEnum.DELIVERY,
        Source = Source5Enum.PROVIDER,
    }
);
```



