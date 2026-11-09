# Product Confirm Response

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRlByb2R1Y3RDb25maXJtUmVzcG9uc2U

The seller's own choice: one of the cards they were shown, or none of them.


# Class Name

`ProductConfirmResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `affectsDecision` | `string` | Required, Constant | Affects decision.<br><br>**Value**: `'False'` | getAffectsDecision(): string | setAffectsDecision(string affectsDecision): void |
| `card` | [ProductCard](http://localhost:3000/llms-pages/php/models/structures/product-card.md) | Required | This is a container for any-of cases. | getCard(): ProductCard | setCard(ProductCard card): void |
| `cardDigest` | string | Required | This is a container for any-of cases. | getCardDigest(): string | setCardDigest(string cardDigest): void |
| `choice` | [`string(Choice2Enum)`](http://localhost:3000/llms-pages/php/models/enumerations/choice-2.md) | Required | Choice. | getChoice(): string | setChoice(string choice): void |
| `confirmedBy` | `string` | Required, Constant | Confirmed by.<br><br>**Value**: `'seller'` | getConfirmedBy(): string | setConfirmedBy(string confirmedBy): void |
| `descriptionDigest` | `string` | Required | Description digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` | getDescriptionDigest(): string | setDescriptionDigest(string descriptionDigest): void |
| `evaluationId` | `string` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` | getEvaluationId(): string | setEvaluationId(string evaluationId): void |
| `recordedAt` | string | Required | This is a container for any-of cases. | getRecordedAt(): string | setRecordedAt(string recordedAt): void |
| `source` | [`string(Source10Enum)`](http://localhost:3000/llms-pages/php/models/enumerations/source-10.md) | Required | Source. | getSource(): string | setSource(string source): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\ProductConfirmResponseBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\ProductCardBuilder;
use TradeGlotLocalConsoleLib\Models\Choice2Enum;
use TradeGlotLocalConsoleLib\Models\Source10Enum;

$productConfirmResponse = ProductConfirmResponseBuilder::init(
    ProductCardBuilder::init(
        'String9',
        'String3',
        'String1',
        [
            'key_features0',
            'key_features1',
            'key_features2'
        ],
        [
            'materials5',
            'materials6'
        ],
        'product_id0',
        'title0'
    )->build(),
    'String1',
    Choice2Enum::CONFIRMED,
    'description_digest2',
    'evaluation_id8',
    'String1',
    Source10Enum::CHANNEL3_LIVE
)->build();
```



