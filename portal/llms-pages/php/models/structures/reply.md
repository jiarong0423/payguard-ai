# Reply

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRlJlcGx5

Reply.


# Class Name

`Reply`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `chooser` | [`?string(ChooserEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/chooser.md) | Optional | Chooser. | getChooser(): ?string | setChooser(?string chooser): void |
| `dropped` | [`?(GuideDropped[])`](http://localhost:3000/llms-pages/php/models/structures/guide-dropped.md) | Optional | Dropped. | getDropped(): ?array | setDropped(?array dropped): void |
| `fallbackReason` | string(Fallback[ReasonEnum](http://localhost:3000/llms-pages/php/models/enumerations/reason.md))\|null | Optional | This is a container for any-of cases. | getFallbackReason(): ?string | setFallbackReason(?string fallbackReason): void |
| `stateChanged` | `?bool` | Optional | State changed. | getStateChanged(): ?bool | setStateChanged(?bool stateChanged): void |
| `template` | [`?string(TemplateEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/template.md) | Optional | Template. | getTemplate(): ?string | setTemplate(?string template): void |
| `text` | `?string` | Optional | Text.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `400` | getText(): ?string | setText(?string text): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\ReplyBuilder;
use TradeGlotLocalConsoleLib\Models\ChooserEnum;
use TradeGlotLocalConsoleLib\Models\Builders\GuideDroppedBuilder;
use TradeGlotLocalConsoleLib\Models\Reason6Enum;
use TradeGlotLocalConsoleLib\Models\FallbackReasonEnum;
use TradeGlotLocalConsoleLib\Models\TemplateEnum;

$reply = ReplyBuilder::init()
    ->chooser(ChooserEnum::KEYWORD)
    ->dropped(
        [
            GuideDroppedBuilder::init(
                'item2',
                Reason6Enum::OTHER_PARTY
            )->build(),
            GuideDroppedBuilder::init(
                'item2',
                Reason6Enum::OTHER_PARTY
            )->build()
        ]
    )
    ->fallbackReason(
        FallbackReasonEnum::PROVIDER_ERROR
    )
    ->stateChanged(false)
    ->template(TemplateEnum::SUBTRACTION)
    ->build();
```



