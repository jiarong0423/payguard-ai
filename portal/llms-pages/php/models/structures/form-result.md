# Form Result

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkZvcm1SZXN1bHQ

Form result.


# Class Name

`FormResult`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `item` | `?string` | Optional | Item. | getItem(): ?string | setItem(?string item): void |
| `valid` | `?bool` | Optional | Valid. | getValid(): ?bool | setValid(?bool valid): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\FormResultBuilder;

$formResult = FormResultBuilder::init()
    ->item('item8')
    ->valid(false)
    ->build();
```



