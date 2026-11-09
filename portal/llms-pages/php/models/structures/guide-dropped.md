# Guide Dropped

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkd1aWRlRHJvcHBlZA

GuideDropped.


# Class Name

`GuideDropped`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `item` | `string` | Required | Item. | getItem(): string | setItem(string item): void |
| `reason` | [`string(Reason6Enum)`](http://localhost:3000/llms-pages/php/models/enumerations/reason-6.md) | Required | Reason. | getReason(): string | setReason(string reason): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\GuideDroppedBuilder;
use TradeGlotLocalConsoleLib\Models\Reason6Enum;

$guideDropped = GuideDroppedBuilder::init(
    'item6',
    Reason6Enum::OTHER_PARTY
)->build();
```



