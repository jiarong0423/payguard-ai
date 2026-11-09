# Evidence Info

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkV2aWRlbmNlSW5mbw

EvidenceInfo.


# Class Name

`EvidenceInfo`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `TrackingInfo` | [`[]models.TrackingInfo`](http://localhost:3000/llms-pages/go/models/structures/tracking-info.md) | Required | Tracking info.<br><br>**Constraints**: *Maximum Items*: `10` |


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



