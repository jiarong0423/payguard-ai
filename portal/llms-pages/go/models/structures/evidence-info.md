# Evidence Info

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkV2aWRlbmNlSW5mbw

EvidenceInfo.


# Class Name

`EvidenceInfo`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `TrackingInfo` | [`[]models.TrackingInfo`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/tracking-info.md) | Required | Tracking info.<br><br>**Constraints**: *Maximum Items*: `10` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    evidenceInfo := models.EvidenceInfo{
        TrackingInfo: []models.TrackingInfo{
            models.TrackingInfo{
                CarrierName:      models.CarrierNameEnum_DHL,
                CarrierNameOther: models.ToPointer(models.TrackingInfoCarrierNameOtherContainer.FromString("String1")),
                TrackingNumber:   "tracking_number6",
            },
        },
    }

}
```



