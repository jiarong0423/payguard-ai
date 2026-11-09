# Guide Field Result

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkd1aWRlRmllbGRSZXN1bHQ

GuideFieldResult.


# Class Name

`GuideFieldResult`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `deferred` | `bool` | Required | Deferred. | getDeferred(): bool | setDeferred(bool deferred): void |
| `item` | `string` | Required | Item. | getItem(): string | setItem(string item): void |
| `valid` | `bool` | Required | Valid. | getValid(): bool | setValid(bool valid): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\GuideFieldResultBuilder;

$guideFieldResult = GuideFieldResultBuilder::init(
    false,
    'item8',
    false
)->build();
```



