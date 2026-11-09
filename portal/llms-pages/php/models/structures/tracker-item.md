# Tracker Item

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRlRyYWNrZXJJdGVt

TrackerItem.


# Class Name

`TrackerItem`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `carrier` | [`string(CarrierEnum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/carrier.md) | Required | Carrier. | getCarrier(): string | setCarrier(string carrier): void |
| `carrierNameOther` | string\|null | Optional | This is a container for any-of cases. | getCarrierNameOther(): ?string | setCarrierNameOther(?string carrierNameOther): void |
| `status` | `string` | Required, Constant | Status.<br><br>**Value**: `'SHIPPED'` | getStatus(): string | setStatus(string status): void |
| `trackingNumber` | `string` | Required | Tracking number.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `64` | getTrackingNumber(): string | setTrackingNumber(string trackingNumber): void |
| `transactionId` | `string` | Required | Transaction id.<br><br>**Constraints**: *Pattern*: `^[A-Za-z0-9*._-]{1,64}$` | getTransactionId(): string | setTransactionId(string transactionId): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\TrackerItemBuilder;
use TradeGlotLocalConsoleLib\Models\CarrierEnum;

$trackerItem = TrackerItemBuilder::init(
    CarrierEnum::TW_CHUNGHWA_POST,
    'tracking_number6',
    'transaction_id6'
)
    ->carrierNameOther(
        'String1'
    )
    ->build();
```



