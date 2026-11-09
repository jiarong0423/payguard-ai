# Guide Field

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkd1aWRlRmllbGQ

GuideField.


# Class Name

`GuideField`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `item` | `string` | Required | Item.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `40`, *Pattern*: `^[a-z_]+$` | getItem(): string | setItem(string item): void |
| `value` | `string` | Required | Value.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `120` | getValue(): string | setValue(string value): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\GuideFieldBuilder;

$guideField = GuideFieldBuilder::init(
    'item8',
    'value8'
)->build();
```



