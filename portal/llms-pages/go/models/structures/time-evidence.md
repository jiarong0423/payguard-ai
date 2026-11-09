# Time Evidence

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRlRpbWVFdmlkZW5jZQ

TimeEvidence.


# Class Name

`TimeEvidence`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AdvisoryOnly` | `string` | Required, Constant | Advisory only.<br><br>**Value**: `"True"` |
| `Events` | [`[]models.TimeEvidenceEvents`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/time-evidence-events.md) | Required | This is Array of a container for any-of cases.<br><br>**Constraints**: *Minimum Items*: `2`, *Maximum Items*: `30` |
| `Flags` | [`[]models.FlagEnum`](http://localhost:3000/llms-pages/go/models/enumerations/flag.md) | Required | Flags.<br><br>**Constraints**: *Maximum Items*: `4` |
| `GapsSeconds` | [`models.TimeGaps`](http://localhost:3000/llms-pages/go/models/structures/time-gaps.md) | Required | TimeGaps. |
| `Judgement` | `string` | Required, Constant | Judgement.<br><br>**Value**: `"NOT_MADE"` |
| `SchemaVersion` | `string` | Required, Constant | Schema version.<br><br>**Value**: `"payguard.time_evidence.v1"` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    timeEvidence := models.TimeEvidence{
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
            models.TimeEvidenceEventsContainer.FromMessageTimeEvent(models.MessageTimeEvent{
                At:                   "at4",
                Channel:              models.ChannelEnum_EMAIL,
                Direction:            models.DirectionEnum_INBOUND,
                Kind:                 "kind6",
                MessageDigest:        "message_digest2",
                Source:               "source4",
                Topic:                models.TopicEnum_ORDERDETAILSPROVIDED,
            }),
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
            models.FlagEnum_DELIVERYAFTERCLAIM,
            models.FlagEnum_CLAIMTIMEEARLIERTHANPAYMENTTIME,
        },
        GapsSeconds:          models.TimeGaps{
            DeliveryToClaim:      models.TimeGapsDeliveryToClaimContainer.FromNumber(210),
            PaymentToClaim:       models.TimeGapsPaymentToClaimContainer.FromNumber(154),
            PaymentToDelivery:    models.TimeGapsPaymentToDeliveryContainer.FromNumber(192),
            PaymentToOrderRecord: models.TimeGapsPaymentToOrderRecordContainer.FromNumber(208),
        },
        Judgement:            "NOT_MADE",
        SchemaVersion:        "payguard.time_evidence.v1",
    }

}
```



