# Tracker Batch

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRlRyYWNrZXJCYXRjaA

TrackerBatch.


# Class Name

`TrackerBatch`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Trackers` | [`[]models.TrackerItem`](http://localhost:3000/llms-pages/go/models/structures/tracker-item.md) | Required | Trackers.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `1` |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    trackerBatch := models.TrackerBatch{
        Trackers: []models.TrackerItem{
            models.TrackerItem{
                Carrier:          models.CarrierEnum_JPJAPANPOST,
                CarrierNameOther: models.ToPointer(models.TrackerItemCarrierNameOtherContainer.FromString("String5")),
                Status:           "SHIPPED",
                TrackingNumber:   "tracking_number0",
                TransactionId:    "transaction_id0",
            },
        },
    }

}
```



