# Time Evidence 1 Events

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRlRpbWVFdmlkZW5jZTFFdmVudHM


# Class Name

`TimeEvidence1Events`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`MessageTimeEvent`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/message-time-event.md) | TimeEvidence1Events.fromMessageTimeEvent(MessageTimeEvent messageTimeEvent) |
| [`TimeEvent`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/time-event.md) | TimeEvidence1Events.fromTimeEvent(TimeEvent timeEvent) |


# MessageTimeEvent

## Initialization Code

### Example

```java
TimeEvidence1Events.fromMessageTimeEvent(
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
TimeEvidence1Events.fromTimeEvent(
        new TimeEvent.Builder(
            "at2",
            KindEnum.DELIVERY,
            Source5Enum.PROVIDER
        )
        .build()
    )
```



