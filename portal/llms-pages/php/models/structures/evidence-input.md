# Evidence Input

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRkV2aWRlbmNlSW5wdXQ

EvidenceInput.


# Class Name

`EvidenceInput`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `evidences` | [`EvidenceInputItem[]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/evidence-input-item.md) | Required | Evidences.<br><br>**Constraints**: *Minimum Items*: `1`, *Maximum Items*: `20` | getEvidences(): array | setEvidences(array evidences): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\EvidenceInputBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\EvidenceInputItemBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\EvidenceInfoBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\TrackingInfoBuilder;
use TradeGlotLocalConsoleLib\Models\CarrierNameEnum;

$evidenceInput = EvidenceInputBuilder::init(
    [
        EvidenceInputItemBuilder::init(
            EvidenceInfoBuilder::init(
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
            )->build(),
            'evidence_type2',
            'notes2'
        )->build()
    ]
)->build();
```



