# Form

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRkZvcm0

Form.


# Class Name

`Form`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `kind` | [`?string(Kind2Enum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/kind-2.md) | Optional | Kind. | getKind(): ?string | setKind(?string kind): void |
| `options` | [`?(GuideOption[])`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/guide-option.md) | Optional | Options. | getOptions(): ?array | setOptions(?array options): void |
| `placeholder` | string\|null | Optional | This is a container for any-of cases. | getPlaceholder(): ?string | setPlaceholder(?string placeholder): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\FormBuilder;
use TradeGlotLocalConsoleLib\Models\Kind2Enum;
use TradeGlotLocalConsoleLib\Models\Builders\GuideOptionBuilder;

$form = FormBuilder::init()
    ->kind(Kind2Enum::TEXT)
    ->options(
        [
            GuideOptionBuilder::init(
                'label2',
                'value4'
            )->build(),
            GuideOptionBuilder::init(
                'label2',
                'value4'
            )->build(),
            GuideOptionBuilder::init(
                'label2',
                'value4'
            )->build()
        ]
    )
    ->placeholder(
        'String9'
    )
    ->build();
```



