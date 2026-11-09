# Time Gaps

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRlRpbWVHYXBz

TimeGaps.


# Class Name

`TimeGaps`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `DeliveryToClaim` | [`models.TimeGapsDeliveryToClaim`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/time-gaps-delivery-to-claim.md) | Required | This is a container for any-of cases. |
| `PaymentToClaim` | [`models.TimeGapsPaymentToClaim`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/time-gaps-payment-to-claim.md) | Required | This is a container for any-of cases. |
| `PaymentToDelivery` | [`models.TimeGapsPaymentToDelivery`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/time-gaps-payment-to-delivery.md) | Required | This is a container for any-of cases. |
| `PaymentToOrderRecord` | [`models.TimeGapsPaymentToOrderRecord`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/time-gaps-payment-to-order-record.md) | Required | This is a container for any-of cases. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    timeGaps := models.TimeGaps{
        DeliveryToClaim:      models.TimeGapsDeliveryToClaimContainer.FromNumber(152),
        PaymentToClaim:       models.TimeGapsPaymentToClaimContainer.FromNumber(212),
        PaymentToDelivery:    models.TimeGapsPaymentToDeliveryContainer.FromNumber(222),
        PaymentToOrderRecord: models.TimeGapsPaymentToOrderRecordContainer.FromNumber(10),
    }

}
```



