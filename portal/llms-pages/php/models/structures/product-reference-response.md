# Product Reference Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRlByb2R1Y3RSZWZlcmVuY2VSZXNwb25zZQ

Up to three Channel3 products for the seller to pick from; advisory, never changes the AUP decision.


# Class Name

`ProductReferenceResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `affectsDecision` | `string` | Required, Constant | Affects decision.<br><br>**Value**: `'False'` | getAffectsDecision(): string | setAffectsDecision(string affectsDecision): void |
| `cards` | [`ProductCard[]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/product-card.md) | Required | Cards.<br><br>**Constraints**: *Maximum Items*: `3` | getCards(): array | setCards(array cards): void |
| `reason` | string([Reason7Enum](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/reason-7.md)) | Required | This is a container for any-of cases. | getReason(): string | setReason(string reason): void |
| `recordedAt` | string | Required | This is a container for any-of cases. | getRecordedAt(): string | setRecordedAt(string recordedAt): void |
| `source` | string([Source11Enum](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/source-11.md)) | Required | This is a container for any-of cases. | getSource(): string | setSource(string source): void |
| `status` | [`string(Status12Enum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/status-12.md) | Required | Status. | getStatus(): string | setStatus(string status): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\ProductReferenceResponseBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\ProductCardBuilder;
use TradeGlotLocalConsoleLib\Models\Reason7Enum;
use TradeGlotLocalConsoleLib\Models\Source11Enum;
use TradeGlotLocalConsoleLib\Models\Status12Enum;

$productReferenceResponse = ProductReferenceResponseBuilder::init(
    [
        ProductCardBuilder::init(
            'String3',
            'String7',
            'String5',
            [
                'key_features4',
                'key_features5',
                'key_features6'
            ],
            [
                'materials9',
                'materials0'
            ],
            'product_id4',
            'title4'
        )->build()
    ],
    Reason7Enum::NOTHING_TO_SEND,
    'String9',
    Source11Enum::CHANNEL3_LIVE,
    Status12Enum::NOT_FOUND
)->build();
```



