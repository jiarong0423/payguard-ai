# Guide Form

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRkd1aWRlRm9ybQ

GuideForm.


# Class Name

`GuideForm`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `kind` | [`string(Kind2Enum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/kind-2.md) | Required | Kind. | getKind(): string | setKind(string kind): void |
| `options` | [`GuideOption[]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/guide-option.md) | Required | Options. | getOptions(): array | setOptions(array options): void |
| `placeholder` | string | Required | This is a container for any-of cases. | getPlaceholder(): string | setPlaceholder(string placeholder): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\GuideFormBuilder;
use TradeGlotLocalConsoleLib\Models\Kind2Enum;
use TradeGlotLocalConsoleLib\Models\Builders\GuideOptionBuilder;

$guideForm = GuideFormBuilder::init(
    Kind2Enum::CHOICE,
    [
        GuideOptionBuilder::init(
            'label2',
            'value4'
        )->build()
    ],
    'String3'
)->build();
```



