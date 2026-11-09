# Time Gaps

Source: http://localhost:3000/#/typescript/x-redirect/JTI0bSUyRlRpbWVHYXBz

TimeGaps.


# Interface Name

`TimeGaps`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `deliveryToClaim` | [`TimeGapsDeliveryToClaim`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/time-gaps-delivery-to-claim.md) | Required | This is a container for any-of cases. |
| `paymentToClaim` | [`TimeGapsPaymentToClaim`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/time-gaps-payment-to-claim.md) | Required | This is a container for any-of cases. |
| `paymentToDelivery` | [`TimeGapsPaymentToDelivery`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/time-gaps-payment-to-delivery.md) | Required | This is a container for any-of cases. |
| `paymentToOrderRecord` | [`TimeGapsPaymentToOrderRecord`](http://localhost:3000/llms-pages/typescript/models/oneof-anyof-definitions/time-gaps-payment-to-order-record.md) | Required | This is a container for any-of cases. |


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



