# Guide Review Request

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkd1aWRlUmV2aWV3UmVxdWVzdA

GuideReviewRequest.


# Class Name

`GuideReviewRequest`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `change` | `?(string[])` | Optional | Change.<br><br>**Constraints**: *Maximum Items*: `9`, *Minimum Length*: `1`, *Maximum Length*: `40`, *Pattern*: `^[a-z_]+$` | getChange(): ?array | setChange(?array change): void |
| `confirm` | `?bool` | Optional | Confirm.<br><br>**Default**: `false` | getConfirm(): ?bool | setConfirm(?bool confirm): void |
| `scenario` | string([Scenario1Enum](http://localhost:3000/llms-pages/php/models/enumerations/scenario-1.md))\|null | Optional | This is a container for any-of cases. | getScenario(): ?string | setScenario(?string scenario): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\GuideReviewRequestBuilder;
use TradeGlotLocalConsoleLib\Models\Scenario1Enum;

$guideReviewRequest = GuideReviewRequestBuilder::init()
    ->change(
        [
            'change9',
            'change0',
            'change1'
        ]
    )
    ->confirm(false)
    ->scenario(
        Scenario1Enum::DISPUTE
    )
    ->build();
```



