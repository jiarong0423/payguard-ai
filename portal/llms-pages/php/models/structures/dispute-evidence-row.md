# Dispute Evidence Row

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRkRpc3B1dGVFdmlkZW5jZVJvdw

DisputeEvidenceRow.


# Class Name

`DisputeEvidenceRow`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `action` | string\|null | Optional | This is a container for any-of cases. | getAction(): ?string | setAction(?string action): void |
| `date` | string\|null | Optional | This is a container for any-of cases. | getDate(): ?string | setDate(?string date): void |
| `evidenceType` | `string` | Required | Evidence type.<br><br>**Constraints**: *Pattern*: `^[A-Z][A-Z0-9_]{0,63}$` | getEvidenceType(): string | setEvidenceType(string evidenceType): void |
| `source` | [`string(Source3Enum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/source-3.md) | Required | Source. | getSource(): string | setSource(string source): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\DisputeEvidenceRowBuilder;
use TradeGlotLocalConsoleLib\Models\Source3Enum;

$disputeEvidenceRow = DisputeEvidenceRowBuilder::init(
    'evidence_type8',
    Source3Enum::REQUESTED_FROM_SELLER
)
    ->action(
        'String7'
    )
    ->date(
        'String3'
    )
    ->build();
```



