# Tracking Info

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRlRyYWNraW5nSW5mbw

TrackingInfo.


# Class Name

`TrackingInfo`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `CarrierName` | [`models.CarrierNameEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/carrier-name.md) | Required | Carrier name. |
| `CarrierNameOther` | [`*models.TrackingInfoCarrierNameOther`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/tracking-info-carrier-name-other.md) | Optional | This is a container for any-of cases. |
| `TrackingNumber` | `string` | Required | Tracking number.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `64` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    trackingInfo := models.TrackingInfo{
        CarrierName:      models.CarrierNameEnum_TWCHUNGHWAPOST,
        CarrierNameOther: models.ToPointer(models.TrackingInfoCarrierNameOtherContainer.FromString("String9")),
        TrackingNumber:   "tracking_number4",
    }

}
```



