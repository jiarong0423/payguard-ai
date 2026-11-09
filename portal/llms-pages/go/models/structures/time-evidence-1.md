# Time Evidence 1

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRlRpbWVFdmlkZW5jZTE

Time evidence.


# Class Name

`TimeEvidence1`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AdvisoryOnly` | `*bool` | Optional | Advisory only. |
| `Events` | [`[]models.TimeEvidence1Events`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/time-evidence-1-events.md) | Optional | This is Array of a container for any-of cases.<br><br>**Constraints**: *Minimum Items*: `2`, *Maximum Items*: `30` |
| `Flags` | [`[]models.FlagEnum`](http://localhost:3000/llms-pages/go/models/enumerations/flag.md) | Optional | Flags.<br><br>**Constraints**: *Maximum Items*: `4` |
| `GapsSeconds` | [`*models.TimeGaps`](http://localhost:3000/llms-pages/go/models/structures/time-gaps.md) | Optional | TimeGaps. |
| `Judgement` | [`*models.JudgementEnum`](http://localhost:3000/llms-pages/go/models/enumerations/judgement.md) | Optional | Judgement. |
| `SchemaVersion` | [`*models.SchemaVersionEnum`](http://localhost:3000/llms-pages/go/models/enumerations/schema-version.md) | Optional | Schema version. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    timeEvidence1 := models.TimeEvidence1{
        AdvisoryOnly:         models.ToPointer(false),
        Events:               []models.TimeEvidence1Events{
            models.TimeEvidence1EventsContainer.FromMessageTimeEvent(models.MessageTimeEvent{
                At:                   "at4",
                Channel:              models.ChannelEnum_EMAIL,
                Direction:            models.DirectionEnum_INBOUND,
                Kind:                 "kind6",
                MessageDigest:        "message_digest2",
                Source:               "source4",
                Topic:                models.TopicEnum_ORDERDETAILSPROVIDED,
            }),
            models.TimeEvidence1EventsContainer.FromMessageTimeEvent(models.MessageTimeEvent{
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
        },
        GapsSeconds:          models.ToPointer(models.TimeGaps{
            DeliveryToClaim:      models.TimeGapsDeliveryToClaimContainer.FromNumber(210),
            PaymentToClaim:       models.TimeGapsPaymentToClaimContainer.FromNumber(154),
            PaymentToDelivery:    models.TimeGapsPaymentToDeliveryContainer.FromNumber(192),
            PaymentToOrderRecord: models.TimeGapsPaymentToOrderRecordContainer.FromNumber(208),
        }),
        Judgement:            models.ToPointer(models.JudgementEnum_NOTMADE),
    }

}
```



