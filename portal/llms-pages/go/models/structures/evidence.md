# Evidence

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkV2aWRlbmNl

Evidence.


# Class Name

`Evidence`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `CarrierStatus` | [`*models.EvidenceCarrierStatus`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/evidence-carrier-status.md) | Optional | This is a container for any-of cases. |
| `DeliveredAt` | [`*models.EvidenceDeliveredAt`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/evidence-delivered-at.md) | Optional | This is a container for any-of cases. |
| `EvidenceSource` | `string` | Required, Constant | Evidence source.<br><br>**Value**: `"synthetic"` |
| `OpenedAt` | [`*models.EvidenceOpenedAt`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/evidence-opened-at.md) | Optional | This is a container for any-of cases. |
| `OrderCreatedAt` | [`*models.EvidenceOrderCreatedAt`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/evidence-order-created-at.md) | Optional | This is a container for any-of cases. |
| `Reason` | [`*models.EvidenceReason`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/evidence-reason.md) | Optional | This is a container for any-of cases. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    evidence := models.Evidence{
        CarrierStatus:  models.ToPointer(models.EvidenceCarrierStatusContainer.FromString("String5")),
        DeliveredAt:    models.ToPointer(models.EvidenceDeliveredAtContainer.FromString("String1")),
        EvidenceSource: "synthetic",
        OpenedAt:       models.ToPointer(models.EvidenceOpenedAtContainer.FromString("String1")),
        OrderCreatedAt: models.ToPointer(models.EvidenceOrderCreatedAtContainer.FromString("String3")),
        Reason:         models.ToPointer(models.EvidenceReasonContainer.FromString("String3")),
    }

}
```



