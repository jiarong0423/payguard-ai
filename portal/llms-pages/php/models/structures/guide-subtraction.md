# Guide Subtraction

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRkd1aWRlU3VidHJhY3Rpb24

GuideSubtraction.


# Class Name

`GuideSubtraction`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `left` | `int` | Required | Left. | getLeft(): int | setLeft(int left): void |
| `needed` | `int` | Required | Needed. | getNeeded(): int | setNeeded(int needed): void |
| `taken` | `int` | Required | Taken. | getTaken(): int | setTaken(int taken): void |
| `text` | `string` | Required | Text. | getText(): string | setText(string text): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\GuideSubtractionBuilder;

$guideSubtraction = GuideSubtractionBuilder::init(
    18,
    112,
    124,
    'text8'
)->build();
```



