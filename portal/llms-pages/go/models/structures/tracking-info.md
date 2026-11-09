# Tracking Info

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRlRyYWNraW5nSW5mbw

TrackingInfo.


# Class Name

`TrackingInfo`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `CarrierName` | [`models.CarrierNameEnum`](http://localhost:3000/llms-pages/go/models/enumerations/carrier-name.md) | Required | Carrier name. |
| `CarrierNameOther` | [`*models.TrackingInfoCarrierNameOther`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/tracking-info-carrier-name-other.md) | Optional | This is a container for any-of cases. |
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



