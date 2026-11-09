# Tracker Batch

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRlRyYWNrZXJCYXRjaA

TrackerBatch.


# Class Name

`TrackerBatch`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `trackers` | [`TrackerItem[]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/tracker-item.md) | Required | Trackers.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `1` | getTrackers(): array | setTrackers(array trackers): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\TrackerBatchBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\TrackerItemBuilder;
use TradeGlotLocalConsoleLib\Models\CarrierEnum;

$trackerBatch = TrackerBatchBuilder::init(
    [
        TrackerItemBuilder::init(
            CarrierEnum::JP_JAPANPOST,
            'tracking_number0',
            'transaction_id0'
        )
            ->carrierNameOther(
                'String5'
            )
            ->build()
    ]
)->build();
```



