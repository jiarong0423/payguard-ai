# Guide Form Result

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRkd1aWRlRm9ybVJlc3VsdA

GuideFormResult.


# Class Name

`GuideFormResult`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `item` | `string` | Required | Item. | getItem(): string | setItem(string item): void |
| `valid` | `bool` | Required | Valid. | getValid(): bool | setValid(bool valid): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\GuideFormResultBuilder;

$guideFormResult = GuideFormResultBuilder::init(
    'item2',
    false
)->build();
```



