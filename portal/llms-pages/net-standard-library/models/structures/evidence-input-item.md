# Evidence Input Item

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkV2aWRlbmNlSW5wdXRJdGVt

EvidenceInputItem.


# Class Name

`EvidenceInputItem`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `EvidenceInfo` | [`EvidenceInfo`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/evidence-info.md) | Required | EvidenceInfo. |
| `EvidenceType` | `string` | Required | Evidence type.<br><br>**Constraints**: *Pattern*: `^[A-Z][A-Z0-9_]{0,63}$` |
| `Notes` | `string` | Required | Notes.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

EvidenceInputItem evidenceInputItem = new EvidenceInputItem
{
    EvidenceInfo = new EvidenceInfo
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
    },
    EvidenceType = "evidence_type2",
    Notes = "notes2",
};
```



