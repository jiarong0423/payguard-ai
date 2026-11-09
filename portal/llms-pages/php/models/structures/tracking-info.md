# Tracking Info

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRlRyYWNraW5nSW5mbw

TrackingInfo.


# Class Name

`TrackingInfo`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `carrierName` | [`string(CarrierNameEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/carrier-name.md) | Required | Carrier name. | getCarrierName(): string | setCarrierName(string carrierName): void |
| `carrierNameOther` | string\|null | Optional | This is a container for any-of cases. | getCarrierNameOther(): ?string | setCarrierNameOther(?string carrierNameOther): void |
| `trackingNumber` | `string` | Required | Tracking number.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `64` | getTrackingNumber(): string | setTrackingNumber(string trackingNumber): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\TrackingInfoBuilder;
use TradeGlotLocalConsoleLib\Models\CarrierNameEnum;

$trackingInfo = TrackingInfoBuilder::init(
    CarrierNameEnum::TW_CHUNGHWA_POST,
    'tracking_number4'
)
    ->carrierNameOther(
        'String9'
    )
    ->build();
```



