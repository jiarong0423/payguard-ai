# Guide Turn Request

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkd1aWRlVHVyblJlcXVlc3Q

GuideTurnRequest.


# Class Name

`GuideTurnRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `fields` | [GuideField](http://localhost:3000/llms-pages/php/models/structures/guide-field.md)[]\|null | Optional | This is a container for any-of cases. | getFields(): ?array | setFields(?array fields): void |
| `scenario` | string([Scenario1Enum](http://localhost:3000/llms-pages/php/models/enumerations/scenario-1.md))\|null | Optional | This is a container for any-of cases. | getScenario(): ?string | setScenario(?string scenario): void |
| `text` | `string` | Required | Text.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `1600` | getText(): string | setText(string text): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\GuideTurnRequestBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\GuideFieldBuilder;
use TradeGlotLocalConsoleLib\Models\Scenario1Enum;

$guideTurnRequest = GuideTurnRequestBuilder::init(
    'text2'
)
    ->fields(
        [
            GuideFieldBuilder::init(
                'item8',
                'value8'
            )->build()
        ]
    )
    ->scenario(
        Scenario1Enum::PREFLIGHT
    )
    ->build();
```



