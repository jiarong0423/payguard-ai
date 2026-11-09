# Time Evidence

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRlRpbWVFdmlkZW5jZQ

TimeEvidence.


# Class Name

`TimeEvidence`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AdvisoryOnly` | `string` | Required, Constant | Advisory only.<br><br>**Value**: `"True"` |
| `Events` | [`List<TimeEvidenceEvents>`](http://localhost:3000/llms-pages/net-standard-library/models/oneof-anyof-definitions/time-evidence-events.md) | Required | This is List of a container for any-of cases.<br><br>**Constraints**: *Minimum Items*: `2`, *Maximum Items*: `30` |
| `Flags` | [`List<FlagEnum>`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/flag.md) | Required | Flags.<br><br>**Constraints**: *Maximum Items*: `4` |
| `GapsSeconds` | [`TimeGaps`](http://localhost:3000/llms-pages/net-standard-library/models/structures/time-gaps.md) | Required | TimeGaps. |
| `Judgement` | `string` | Required, Constant | Judgement.<br><br>**Value**: `"NOT_MADE"` |
| `SchemaVersion` | `string` | Required, Constant | Schema version.<br><br>**Value**: `"payguard.time_evidence.v1"` |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

TimeEvidence timeEvidence = new TimeEvidence
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
        FlagEnum.DELIVERYAFTERCLAIM,
        FlagEnum.CLAIMTIMEEARLIERTHANPAYMENTTIME,
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
};
```



