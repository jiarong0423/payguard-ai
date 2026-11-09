# Dispute Draft Response Time Evidence

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRkRpc3B1dGVEcmFmdFJlc3BvbnNlVGltZUV2aWRlbmNl


# Data Type

`TimeEvidence`


# Cases

| Type |
|  --- |
| [`TimeEvidence`](http://localhost:3000/llms-pages/python/models/structures/time-evidence.md) |


# TimeEvidence

## Initialization Code

### Example

```python
value = TimeEvidence(
    events=[
        MessageTimeEvent(
            at='at4',
            channel=ChannelEnum.EMAIL,
            direction=DirectionEnum.INBOUND,
            message_digest='message_digest2',
            topic=TopicEnum.ORDER_DETAILS_PROVIDED
        )
    ],
    flags=[
        FlagEnum.ORDER_RECORD_ABSENT,
        FlagEnum.DELIVERY_NOT_RECORDED,
        FlagEnum.DELIVERY_AFTER_CLAIM
    ],
    gaps_seconds=TimeGaps(
        delivery_to_claim=210,
        payment_to_claim=154,
        payment_to_delivery=192,
        payment_to_order_record=208
    )
)
```



