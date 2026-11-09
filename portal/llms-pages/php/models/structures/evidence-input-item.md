# Evidence Input Item

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkV2aWRlbmNlSW5wdXRJdGVt

EvidenceInputItem.


# Class Name

`EvidenceInputItem`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `evidenceInfo` | [`EvidenceInfo`](http://localhost:3000/llms-pages/php/models/structures/evidence-info.md) | Required | EvidenceInfo. | getEvidenceInfo(): EvidenceInfo | setEvidenceInfo(EvidenceInfo evidenceInfo): void |
| `evidenceType` | `string` | Required | Evidence type.<br><br>**Constraints**: *Pattern*: `^[A-Z][A-Z0-9_]{0,63}$` | getEvidenceType(): string | setEvidenceType(string evidenceType): void |
| `notes` | `string` | Required | Notes.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `2000` | getNotes(): string | setNotes(string notes): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\EvidenceInputItemBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\EvidenceInfoBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\TrackingInfoBuilder;
use TradeGlotLocalConsoleLib\Models\CarrierNameEnum;

$evidenceInputItem = EvidenceInputItemBuilder::init(
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
)->build();
```



