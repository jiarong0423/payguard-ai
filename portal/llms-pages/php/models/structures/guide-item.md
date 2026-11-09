# Guide Item

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRkd1aWRlSXRlbQ

GuideItem.


# Class Name

`GuideItem`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `chunk` | string | Required | This is a container for any-of cases. | getChunk(): string | setChunk(string chunk): void |
| `form` | [GuideForm](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/guide-form.md) | Required | This is a container for any-of cases. | getForm(): GuideForm | setForm(GuideForm form): void |
| `id` | `string` | Required | Id. | getId(): string | setId(string id): void |
| `label` | `string` | Required | Label. | getLabel(): string | setLabel(string label): void |
| `source` | [`string(Source8Enum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/source-8.md) | Required | Source. | getSource(): string | setSource(string source): void |
| `status` | [`string(Status9Enum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/status-9.md) | Required | Status. | getStatus(): string | setStatus(string status): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\GuideItemBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\GuideFormBuilder;
use TradeGlotLocalConsoleLib\Models\Kind2Enum;
use TradeGlotLocalConsoleLib\Models\Builders\GuideOptionBuilder;
use TradeGlotLocalConsoleLib\Models\Source8Enum;
use TradeGlotLocalConsoleLib\Models\Status9Enum;

$guideItem = GuideItemBuilder::init(
    'String7',
    GuideFormBuilder::init(
        Kind2Enum::CHOICE,
        [
            GuideOptionBuilder::init(
                'label2',
                'value4'
            )->build()
        ],
        'String9'
    )->build(),
    'id0',
    'label0',
    Source8Enum::OFFICIAL,
    Status9Enum::UNCLEAR
)->build();
```



