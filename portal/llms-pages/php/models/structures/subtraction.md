# Subtraction

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRlN1YnRyYWN0aW9u

Subtraction.


# Class Name

`Subtraction`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `left` | `?int` | Optional | Left. | getLeft(): ?int | setLeft(?int left): void |
| `needed` | `?int` | Optional | Needed. | getNeeded(): ?int | setNeeded(?int needed): void |
| `taken` | `?int` | Optional | Taken. | getTaken(): ?int | setTaken(?int taken): void |
| `text` | `?string` | Optional | Text. | getText(): ?string | setText(?string text): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\SubtractionBuilder;

$subtraction = SubtractionBuilder::init()
    ->left(232)
    ->needed(102)
    ->taken(90)
    ->text('text6')
    ->build();
```



