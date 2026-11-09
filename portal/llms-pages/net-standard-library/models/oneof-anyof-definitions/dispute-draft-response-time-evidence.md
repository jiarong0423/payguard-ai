# Dispute Draft Response Time Evidence

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkRpc3B1dGVEcmFmdFJlc3BvbnNlVGltZUV2aWRlbmNl


# Class Name

`DisputeDraftResponseTimeEvidence`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`TimeEvidence`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/time-evidence.md) | DisputeDraftResponseTimeEvidence.FromTimeEvidence(TimeEvidence timeEvidence) |


# TimeEvidence

## Initialization Code

### Example

```csharp
DisputeDraftResponseTimeEvidence value = DisputeDraftResponseTimeEvidence.FromTimeEvidence(
    new TimeEvidence
    {
        AdvisoryOnly = "True",
        Events = new List<TimeEvidenceEvents>
        {
            TimeEvidenceEvents.FromMessageTimeEvent(
                new MessageTimeEvent
                {
                    At = "at4",
                    Channel = ChannelEnum.EMAIL,
                    Direction = DirectionEnum.INBOUND,
                    Kind = "kind6",
                    MessageDigest = "message_digest2",
                    Source = "source4",
                    Topic = TopicEnum.ORDERDETAILSPROVIDED,
                }
            ),
        },
        Flags = new List<FlagEnum>
        {
            FlagEnum.ORDERRECORDABSENT,
            FlagEnum.DELIVERYNOTRECORDED,
            FlagEnum.DELIVERYAFTERCLAIM,
        },
        GapsSeconds = new TimeGaps
        {
            DeliveryToClaim = TimeGapsDeliveryToClaim.FromNumber(210),
            PaymentToClaim = TimeGapsPaymentToClaim.FromNumber(154),
            PaymentToDelivery = TimeGapsPaymentToDelivery.FromNumber(192),
            PaymentToOrderRecord = TimeGapsPaymentToOrderRecord.FromNumber(208),
        },
        Judgement = "NOT_MADE",
        SchemaVersion = "payguard.time_evidence.v1",
    }
);
```



