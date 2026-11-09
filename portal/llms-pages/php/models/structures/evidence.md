# Evidence

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkV2aWRlbmNl

Evidence.


# Class Name

`Evidence`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `carrierStatus` | string\|null | Optional | This is a container for any-of cases. | getCarrierStatus(): ?string | setCarrierStatus(?string carrierStatus): void |
| `deliveredAt` | string\|null | Optional | This is a container for any-of cases. | getDeliveredAt(): ?string | setDeliveredAt(?string deliveredAt): void |
| `evidenceSource` | `string` | Required, Constant | Evidence source.<br><br>**Value**: `'synthetic'` | getEvidenceSource(): string | setEvidenceSource(string evidenceSource): void |
| `openedAt` | string\|null | Optional | This is a container for any-of cases. | getOpenedAt(): ?string | setOpenedAt(?string openedAt): void |
| `orderCreatedAt` | string\|null | Optional | This is a container for any-of cases. | getOrderCreatedAt(): ?string | setOrderCreatedAt(?string orderCreatedAt): void |
| `reason` | string\|null | Optional | This is a container for any-of cases. | getReason(): ?string | setReason(?string reason): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\EvidenceBuilder;

$evidence = EvidenceBuilder::init()
    ->carrierStatus(
        'String5'
    )
    ->deliveredAt(
        'String1'
    )
    ->openedAt(
        'String1'
    )
    ->orderCreatedAt(
        'String3'
    )
    ->reason(
        'String3'
    )
    ->build();
```



