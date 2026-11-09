# Time Gaps

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRlRpbWVHYXBz

TimeGaps.


# Class Name

`TimeGaps`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `DeliveryToClaim` | [`models.TimeGapsDeliveryToClaim`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/time-gaps-delivery-to-claim.md) | Required | This is a container for any-of cases. |
| `PaymentToClaim` | [`models.TimeGapsPaymentToClaim`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/time-gaps-payment-to-claim.md) | Required | This is a container for any-of cases. |
| `PaymentToDelivery` | [`models.TimeGapsPaymentToDelivery`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/time-gaps-payment-to-delivery.md) | Required | This is a container for any-of cases. |
| `PaymentToOrderRecord` | [`models.TimeGapsPaymentToOrderRecord`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/time-gaps-payment-to-order-record.md) | Required | This is a container for any-of cases. |


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



