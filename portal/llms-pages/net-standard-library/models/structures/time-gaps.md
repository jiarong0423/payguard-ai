# Time Gaps

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRlRpbWVHYXBz

TimeGaps.


# Class Name

`TimeGaps`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `DeliveryToClaim` | [`TimeGapsDeliveryToClaim`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/time-gaps-delivery-to-claim.md) | Required | This is a container for any-of cases. |
| `PaymentToClaim` | [`TimeGapsPaymentToClaim`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/time-gaps-payment-to-claim.md) | Required | This is a container for any-of cases. |
| `PaymentToDelivery` | [`TimeGapsPaymentToDelivery`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/time-gaps-payment-to-delivery.md) | Required | This is a container for any-of cases. |
| `PaymentToOrderRecord` | [`TimeGapsPaymentToOrderRecord`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/time-gaps-payment-to-order-record.md) | Required | This is a container for any-of cases. |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

TimeGaps timeGaps = new TimeGaps
{
    DeliveryToClaim = TimeGapsDeliveryToClaim.FromNumber(152),
    PaymentToClaim = TimeGapsPaymentToClaim.FromNumber(212),
    PaymentToDelivery = TimeGapsPaymentToDelivery.FromNumber(222),
    PaymentToOrderRecord = TimeGapsPaymentToOrderRecord.FromNumber(10),
};
```



