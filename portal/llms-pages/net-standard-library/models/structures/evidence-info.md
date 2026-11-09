# Evidence Info

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkV2aWRlbmNlSW5mbw

EvidenceInfo.


# Class Name

`EvidenceInfo`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `TrackingInfo` | [`List<TrackingInfo>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/tracking-info.md) | Required | Tracking info.<br><br>**Constraints**: *Maximum Items*: `10` |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

EvidenceInfo evidenceInfo = new EvidenceInfo
{
    TrackingInfo = new List<TrackingInfo>
    {
        new TrackingInfo
        {
            CarrierName = CarrierNameEnum.DHL,
            TrackingNumber = "tracking_number6",
            CarrierNameOther = TrackingInfoCarrierNameOther.FromString("String1"),
        },
    },
};
```



