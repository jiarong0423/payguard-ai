# Guide Option

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRkd1aWRlT3B0aW9u

GuideOption.


# Class Name

`GuideOption`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `label` | `string` | Required | Label. | getLabel(): string | setLabel(string label): void |
| `value` | `string` | Required | Value. | getValue(): string | setValue(string value): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\GuideOptionBuilder;

$guideOption = GuideOptionBuilder::init(
    'label2',
    'value4'
)->build();
```



