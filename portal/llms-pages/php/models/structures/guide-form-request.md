# Guide Form Request

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkd1aWRlRm9ybVJlcXVlc3Q

One field ({item, value}) or one round of up to three fields ({fields: [...]}), never both.


# Class Name

`GuideFormRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `confirmReview` | `?bool` | Optional | Confirm review.<br><br>**Default**: `false` | getConfirmReview(): ?bool | setConfirmReview(?bool confirmReview): void |
| `fields` | [GuideField](http://localhost:3000/llms-pages/php/models/structures/guide-field.md)[]\|null | Optional | This is a container for any-of cases. | getFields(): ?array | setFields(?array fields): void |
| `item` | string\|null | Optional | This is a container for any-of cases. | getItem(): ?string | setItem(?string item): void |
| `scenario` | string([Scenario1Enum](http://localhost:3000/llms-pages/php/models/enumerations/scenario-1.md))\|null | Optional | This is a container for any-of cases. | getScenario(): ?string | setScenario(?string scenario): void |
| `value` | string\|null | Optional | This is a container for any-of cases. | getValue(): ?string | setValue(?string value): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\GuideFormRequestBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\GuideFieldBuilder;
use TradeGlotLocalConsoleLib\Models\Scenario1Enum;

$guideFormRequest = GuideFormRequestBuilder::init()
    ->confirmReview(false)
    ->fields(
        [
            GuideFieldBuilder::init(
                'item8',
                'value8'
            )->build()
        ]
    )
    ->item(
        'String1'
    )
    ->scenario(
        Scenario1Enum::PREFLIGHT
    )
    ->value(
        'String1'
    )
    ->build();
```



