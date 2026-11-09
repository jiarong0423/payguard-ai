# Evidence Input

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkV2aWRlbmNlSW5wdXQ

EvidenceInput.


# Class Name

`EvidenceInput`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Evidences` | [`List<EvidenceInputItem>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/evidence-input-item.md) | Required | Evidences.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `20` |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

EvidenceInput evidenceInput = new EvidenceInput
{
    Evidences = new List<EvidenceInputItem>
    {
        new EvidenceInputItem
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
        },
    },
};
```



