# Time Gaps

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRlRpbWVHYXBz

TimeGaps.


# Interface Name

`TimeGaps`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `deliveryToClaim` | [`TimeGapsDeliveryToClaim`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/time-gaps-delivery-to-claim.md) | Required | This is a container for any-of cases. |
| `paymentToClaim` | [`TimeGapsPaymentToClaim`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/time-gaps-payment-to-claim.md) | Required | This is a container for any-of cases. |
| `paymentToDelivery` | [`TimeGapsPaymentToDelivery`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/time-gaps-payment-to-delivery.md) | Required | This is a container for any-of cases. |
| `paymentToOrderRecord` | [`TimeGapsPaymentToOrderRecord`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/time-gaps-payment-to-order-record.md) | Required | This is a container for any-of cases. |


# Example

```ts
import { TimeGaps } from 'tradeglot-local-consolelib';

const timeGaps: TimeGaps = {
  deliveryToClaim: 152,
  paymentToClaim: 212,
  paymentToDelivery: 222,
  paymentToOrderRecord: 10,
};
```



