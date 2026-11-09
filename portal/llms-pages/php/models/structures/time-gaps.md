# Time Gaps

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRlRpbWVHYXBz

TimeGaps.


# Class Name

`TimeGaps`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `deliveryToClaim` | int | Required | This is a container for any-of cases. | getDeliveryToClaim(): int | setDeliveryToClaim(int deliveryToClaim): void |
| `paymentToClaim` | int | Required | This is a container for any-of cases. | getPaymentToClaim(): int | setPaymentToClaim(int paymentToClaim): void |
| `paymentToDelivery` | int | Required | This is a container for any-of cases. | getPaymentToDelivery(): int | setPaymentToDelivery(int paymentToDelivery): void |
| `paymentToOrderRecord` | int | Required | This is a container for any-of cases. | getPaymentToOrderRecord(): int | setPaymentToOrderRecord(int paymentToOrderRecord): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\TimeGapsBuilder;

$timeGaps = TimeGapsBuilder::init(
    152,
    212,
    222,
    10
)->build();
```



