# Time Evidence 1

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRlRpbWVFdmlkZW5jZTE

Time evidence.


# Class Name

`TimeEvidence1`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AdvisoryOnly` | `bool?` | Optional | Advisory only. |
| `Events` | [`List<TimeEvidence1Events>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/time-evidence-1-events.md) | Optional | This is List of a container for any-of cases.<br><br>**Constraints**: *Minimum Items*: `2`, *Maximum Items*: `30` |
| `Flags` | [`List<FlagEnum>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/flag.md) | Optional | Flags.<br><br>**Constraints**: *Maximum Items*: `4` |
| `GapsSeconds` | [`TimeGaps`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/time-gaps.md) | Optional | TimeGaps. |
| `Judgement` | [`JudgementEnum?`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/judgement.md) | Optional | Judgement. |
| `SchemaVersion` | [`SchemaVersionEnum?`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/schema-version.md) | Optional | Schema version. |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

TimeEvidence1 timeEvidence1 = new TimeEvidence1
{
    AdvisoryOnly = false,
    Events = new List<TimeEvidence1Events>
    {
        TimeEvidence1Events.FromMessageTimeEvent(
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
        TimeEvidence1Events.FromMessageTimeEvent(
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
    },
    GapsSeconds = new TimeGaps
    {
        DeliveryToClaim = TimeGapsDeliveryToClaim.FromNumber(210),
        PaymentToClaim = TimeGapsPaymentToClaim.FromNumber(154),
        PaymentToDelivery = TimeGapsPaymentToDelivery.FromNumber(192),
        PaymentToOrderRecord = TimeGapsPaymentToOrderRecord.FromNumber(208),
    },
    Judgement = JudgementEnum.NOTMADE,
};
```



