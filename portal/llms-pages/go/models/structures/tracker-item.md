# Tracker Item

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRlRyYWNrZXJJdGVt

TrackerItem.


# Class Name

`TrackerItem`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Carrier` | [`models.CarrierEnum`](http://localhost:3000/llms-pages/go/models/enumerations/carrier.md) | Required | Carrier. |
| `CarrierNameOther` | [`*models.TrackerItemCarrierNameOther`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/tracker-item-carrier-name-other.md) | Optional | This is a container for any-of cases. |
| `Status` | `string` | Required, Constant | Status.<br><br>**Value**: `"SHIPPED"` |
| `TrackingNumber` | `string` | Required | Tracking number.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `64` |
| `TransactionId` | `string` | Required | Transaction id.<br><br>**Constraints**: *Pattern*: `^[A-Za-z0-9*._-]{1,64}$` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    trackerItem := models.TrackerItem{
        Carrier:          models.CarrierEnum_TWCHUNGHWAPOST,
        CarrierNameOther: models.ToPointer(models.TrackerItemCarrierNameOtherContainer.FromString("String1")),
        Status:           "SHIPPED",
        TrackingNumber:   "tracking_number6",
        TransactionId:    "transaction_id6",
    }

}
```



