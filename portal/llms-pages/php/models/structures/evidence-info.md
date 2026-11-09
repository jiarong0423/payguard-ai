# Evidence Info

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRkV2aWRlbmNlSW5mbw

EvidenceInfo.


# Class Name

`EvidenceInfo`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `trackingInfo` | [`TrackingInfo[]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/tracking-info.md) | Required | Tracking info.<br><br>**Constraints**: *Maximum Items*: `10` | getTrackingInfo(): array | setTrackingInfo(array trackingInfo): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\EvidenceInfoBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\TrackingInfoBuilder;
use TradeGlotLocalConsoleLib\Models\CarrierNameEnum;

$evidenceInfo = EvidenceInfoBuilder::init(
    [
        TrackingInfoBuilder::init(
            CarrierNameEnum::DHL,
            'tracking_number6'
        )
            ->carrierNameOther(
                'String1'
            )
            ->build()
    ]
)->build();
```



