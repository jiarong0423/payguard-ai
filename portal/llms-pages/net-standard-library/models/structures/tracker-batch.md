# Tracker Batch

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRlRyYWNrZXJCYXRjaA

TrackerBatch.


# Class Name

`TrackerBatch`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Trackers` | [`List<TrackerItem>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/tracker-item.md) | Required | Trackers.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `1` |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

TrackerBatch trackerBatch = new TrackerBatch
{
    Trackers = new List<TrackerItem>
    {
        new TrackerItem
        {
            Carrier = CarrierEnum.JPJAPANPOST,
            Status = "SHIPPED",
            TrackingNumber = "tracking_number0",
            TransactionId = "transaction_id0",
            CarrierNameOther = TrackerItemCarrierNameOther.FromString("String5"),
        },
    },
};
```



