# Dispute Draft Response Time Evidence

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkRpc3B1dGVEcmFmdFJlc3BvbnNlVGltZUV2aWRlbmNl


# Class Name

`DisputeDraftResponseTimeEvidence`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`TimeEvidence`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/time-evidence.md) | DisputeDraftResponseTimeEvidence.fromTimeEvidence(TimeEvidence timeEvidence) |


# TimeEvidence

## Initialization Code

### Example

```java
DisputeDraftResponseTimeEvidence.fromTimeEvidence(
        new TimeEvidence.Builder(
            "True",
            Arrays.asList(
                TimeEvidenceEvents.fromMessageTimeEvent(
                    new MessageTimeEvent.Builder(
                        "at4",
                        ChannelEnum.EMAIL,
                        DirectionEnum.INBOUND,
                        "kind6",
                        "message_digest2",
                        "source4",
                        TopicEnum.ORDER_DETAILS_PROVIDED
                    )
                    .build()
                )
            ),
            Arrays.asList(
                FlagEnum.ORDER_RECORD_ABSENT,
                FlagEnum.DELIVERY_NOT_RECORDED,
                FlagEnum.DELIVERY_AFTER_CLAIM
            ),
            new TimeGaps.Builder(
                TimeGapsDeliveryToClaim.fromNumber(
                    210
                ),
                TimeGapsPaymentToClaim.fromNumber(
                    154
                ),
                TimeGapsPaymentToDelivery.fromNumber(
                    192
                ),
                TimeGapsPaymentToOrderRecord.fromNumber(
                    208
                )
            )
            .build(),
            "NOT_MADE",
            "payguard.time_evidence.v1"
        )
        .build()
    )
```



