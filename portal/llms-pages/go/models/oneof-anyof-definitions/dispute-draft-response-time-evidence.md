# Dispute Draft Response Time Evidence

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkRpc3B1dGVEcmFmdFJlc3BvbnNlVGltZUV2aWRlbmNl


# Class Name

`DisputeDraftResponseTimeEvidence`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`models.TimeEvidence`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/time-evidence.md) | models.DisputeDraftResponseTimeEvidenceContainer.FromTimeEvidence(models.TimeEvidence timeEvidence) |


# models.TimeEvidence

## Initialization Code

### Example

```go
value := models.DisputeDraftResponseTimeEvidenceContainer.FromTimeEvidence(models.TimeEvidence{
    AdvisoryOnly:         "True",
    Events:               []models.TimeEvidenceEvents{
        models.TimeEvidenceEventsContainer.FromMessageTimeEvent(models.MessageTimeEvent{
            At:                   "at4",
            Channel:              models.ChannelEnum_EMAIL,
            Direction:            models.DirectionEnum_INBOUND,
            Kind:                 "kind6",
            MessageDigest:        "message_digest2",
            Source:               "source4",
            Topic:                models.TopicEnum_ORDERDETAILSPROVIDED,
        }),
    },
    Flags:                []models.FlagEnum{
        models.FlagEnum_ORDERRECORDABSENT,
        models.FlagEnum_DELIVERYNOTRECORDED,
        models.FlagEnum_DELIVERYAFTERCLAIM,
    },
    GapsSeconds:          models.TimeGaps{
        DeliveryToClaim:      models.TimeGapsDeliveryToClaimContainer.FromNumber(210),
        PaymentToClaim:       models.TimeGapsPaymentToClaimContainer.FromNumber(154),
        PaymentToDelivery:    models.TimeGapsPaymentToDeliveryContainer.FromNumber(192),
        PaymentToOrderRecord: models.TimeGapsPaymentToOrderRecordContainer.FromNumber(208),
    },
    Judgement:            "NOT_MADE",
    SchemaVersion:        "payguard.time_evidence.v1",
})
```



