# Guide Reply

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkd1aWRlUmVwbHk

GuideReply.


# Class Name

`GuideReply`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `chooser` | [`string(ChooserEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/chooser.md) | Required | Chooser. | getChooser(): string | setChooser(string chooser): void |
| `dropped` | [`GuideDropped[]`](http://localhost:3000/llms-pages/php/models/structures/guide-dropped.md) | Required | Dropped. | getDropped(): array | setDropped(array dropped): void |
| `fallbackReason` | string(Fallback[ReasonEnum](http://localhost:3000/llms-pages/php/models/enumerations/reason.md)) | Required | This is a container for any-of cases. | getFallbackReason(): string | setFallbackReason(string fallbackReason): void |
| `stateChanged` | `bool` | Required | State changed. | getStateChanged(): bool | setStateChanged(bool stateChanged): void |
| `template` | [`string(TemplateEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/template.md) | Required | Template. | getTemplate(): string | setTemplate(string template): void |
| `text` | `string` | Required | Text.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `400` | getText(): string | setText(string text): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\GuideReplyBuilder;
use TradeGlotLocalConsoleLib\Models\ChooserEnum;
use TradeGlotLocalConsoleLib\Models\Builders\GuideDroppedBuilder;
use TradeGlotLocalConsoleLib\Models\Reason6Enum;
use TradeGlotLocalConsoleLib\Models\FallbackReasonEnum;
use TradeGlotLocalConsoleLib\Models\TemplateEnum;

$guideReply = GuideReplyBuilder::init(
    ChooserEnum::NONE,
    [
        GuideDroppedBuilder::init(
            'item2',
            Reason6Enum::OTHER_PARTY
        )->build()
    ],
    FallbackReasonEnum::LATE,
    false,
    TemplateEnum::NO_GUARANTEE,
    'text6'
)->build();
```



