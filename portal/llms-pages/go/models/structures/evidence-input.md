# Evidence Input

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkV2aWRlbmNlSW5wdXQ

EvidenceInput.


# Class Name

`EvidenceInput`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Evidences` | [`[]models.EvidenceInputItem`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/evidence-input-item.md) | Required | Evidences.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `20` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    evidenceInput := models.EvidenceInput{
        Evidences: []models.EvidenceInputItem{
            models.EvidenceInputItem{
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
            },
        },
    }

}
```



