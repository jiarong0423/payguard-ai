# Time Evidence Events

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRlRpbWVFdmlkZW5jZUV2ZW50cw


# Class Name

`TimeEvidenceEvents`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`MessageTimeEvent`](http://localhost:3000/llms-pages/java/models/structures/message-time-event.md) | TimeEvidenceEvents.fromMessageTimeEvent(MessageTimeEvent messageTimeEvent) |
| [`TimeEvent`](http://localhost:3000/llms-pages/java/models/structures/time-event.md) | TimeEvidenceEvents.fromTimeEvent(TimeEvent timeEvent) |


# MessageTimeEvent

## Initialization Code

### Example

```java
TimeEvidenceEvents.fromMessageTimeEvent(
        new MessageTimeEvent.Builder(
            "at4",
            ChannelEnum.EMAIL,
            DirectionEnum.INBOUND,
            "MESSAGE",
            "message_digest2",
            "SELLER_PROVIDED_UNVERIFIED",
            TopicEnum.ORDER_DETAILS_PROVIDED
        )
        .build()
    )
```


# TimeEvent

## Initialization Code

### Example

```java
TimeEvidenceEvents.fromTimeEvent(
        new TimeEvent.Builder(
            "at2",
            KindEnum.DELIVERY,
            Source5Enum.PROVIDER
        )
        .build()
    )
```



