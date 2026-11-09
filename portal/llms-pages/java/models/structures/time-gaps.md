# Time Gaps

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRlRpbWVHYXBz

TimeGaps.


# Class Name

`TimeGaps`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `DeliveryToClaim` | [`TimeGapsDeliveryToClaim`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/time-gaps-delivery-to-claim.md) | Required | This is a container for any-of cases. | TimeGapsDeliveryToClaim getDeliveryToClaim() | setDeliveryToClaim(TimeGapsDeliveryToClaim deliveryToClaim) |
| `PaymentToClaim` | [`TimeGapsPaymentToClaim`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/time-gaps-payment-to-claim.md) | Required | This is a container for any-of cases. | TimeGapsPaymentToClaim getPaymentToClaim() | setPaymentToClaim(TimeGapsPaymentToClaim paymentToClaim) |
| `PaymentToDelivery` | [`TimeGapsPaymentToDelivery`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/time-gaps-payment-to-delivery.md) | Required | This is a container for any-of cases. | TimeGapsPaymentToDelivery getPaymentToDelivery() | setPaymentToDelivery(TimeGapsPaymentToDelivery paymentToDelivery) |
| `PaymentToOrderRecord` | [`TimeGapsPaymentToOrderRecord`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/time-gaps-payment-to-order-record.md) | Required | This is a container for any-of cases. | TimeGapsPaymentToOrderRecord getPaymentToOrderRecord() | setPaymentToOrderRecord(TimeGapsPaymentToOrderRecord paymentToOrderRecord) |


# Example

```java
import m18000.m0.m0.m127.models.TimeGaps;
import m18000.m0.m0.m127.models.containers.TimeGapsDeliveryToClaim;
import m18000.m0.m0.m127.models.containers.TimeGapsPaymentToClaim;
import m18000.m0.m0.m127.models.containers.TimeGapsPaymentToDelivery;
import m18000.m0.m0.m127.models.containers.TimeGapsPaymentToOrderRecord;

TimeGaps timeGaps = new TimeGaps.Builder(
    TimeGapsDeliveryToClaim.fromNumber(
        152
    ),
    TimeGapsPaymentToClaim.fromNumber(
        212
    ),
    TimeGapsPaymentToDelivery.fromNumber(
        222
    ),
    TimeGapsPaymentToOrderRecord.fromNumber(
        10
    )
)
.build();
```



