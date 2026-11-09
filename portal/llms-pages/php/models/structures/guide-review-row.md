# Guide Review Row

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkd1aWRlUmV2aWV3Um93

GuideReviewRow.


# Class Name

`GuideReviewRow`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `item` | `string` | Required | Item. | getItem(): string | setItem(string item): void |
| `source` | [`string(Source9Enum)`](http://localhost:3000/llms-pages/php/models/enumerations/source-9.md) | Required | Source. | getSource(): string | setSource(string source): void |
| `value` | `string` | Required | Value.<br><br>**Constraints**: *Maximum Length*: `120` | getValue(): string | setValue(string value): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\GuideReviewRowBuilder;
use TradeGlotLocalConsoleLib\Models\Source9Enum;

$guideReviewRow = GuideReviewRowBuilder::init(
    'item6',
    Source9Enum::WORDS,
    'value6'
)->build();
```



