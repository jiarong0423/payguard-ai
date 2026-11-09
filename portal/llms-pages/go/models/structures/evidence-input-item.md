# Evidence Input Item

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkV2aWRlbmNlSW5wdXRJdGVt

EvidenceInputItem.


# Class Name

`EvidenceInputItem`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `EvidenceInfo` | [`models.EvidenceInfo`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/evidence-info.md) | Required | EvidenceInfo. |
| `EvidenceType` | `string` | Required | Evidence type.<br><br>**Constraints**: *Pattern*: `^[A-Z][A-Z0-9_]{0,63}$` |
| `Notes` | `string` | Required | Notes.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    evidenceInputItem := models.EvidenceInputItem{
        EvidenceInfo: models.EvidenceInfo{
            TrackingInfo: []models.TrackingInfo{
                models.TrackingInfo{
                    CarrierName:      models.CarrierNameEnum_DHL,
                    CarrierNameOther: models.ToPointer(models.TrackingInfoCarrierNameOtherContainer.FromString("String1")),
                    TrackingNumber:   "tracking_number6",
                },
            },
        },
        EvidenceType: "evidence_type2",
        Notes:        "notes2",
    }

}
```



