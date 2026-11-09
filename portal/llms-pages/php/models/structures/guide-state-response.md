# Guide State Response

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkd1aWRlU3RhdGVSZXNwb25zZQ

GuideStateResponse.


# Class Name

`GuideStateResponse`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `advisoryOnly` | `string` | Required, Constant | Advisory only.<br><br>**Value**: `'True'` | getAdvisoryOnly(): string | setAdvisoryOnly(string advisoryOnly): void |
| `analysis` | [GuideAnalysis](http://localhost:3000/llms-pages/php/models/structures/guide-analysis.md) | Required | This is a container for any-of cases. | getAnalysis(): GuideAnalysis | setAnalysis(GuideAnalysis analysis): void |
| `asked` | `string[]` | Required | Asked.<br><br>**Constraints**: *Maximum Items*: `3` | getAsked(): array | setAsked(array asked): void |
| `autoConfirmed` | `string[]` | Required | Auto confirmed. | getAutoConfirmed(): array | setAutoConfirmed(array autoConfirmed): void |
| `chooserMode` | [`string(ChooserModeEnum)`](http://localhost:3000/llms-pages/php/models/enumerations/chooser-mode.md) | Required | Chooser mode. | getChooserMode(): string | setChooserMode(string chooserMode): void |
| `deferred` | `string[]` | Required | Deferred. | getDeferred(): array | setDeferred(array deferred): void |
| `flowName` | string | Required | This is a container for any-of cases. | getFlowName(): string | setFlowName(string flowName): void |
| `formResult` | [GuideForm](http://localhost:3000/llms-pages/php/models/structures/guide-form.md)Result | Required | This is a container for any-of cases. | getFormResult(): GuideFormResult | setFormResult(GuideFormResult formResult): void |
| `formResults` | [`GuideFieldResult[]`](http://localhost:3000/llms-pages/php/models/structures/guide-field-result.md) | Required | Form results. | getFormResults(): array | setFormResults(array formResults): void |
| `gap` | [`GuideGap`](http://localhost:3000/llms-pages/php/models/structures/guide-gap.md) | Required | GuideGap. | getGap(): GuideGap | setGap(GuideGap gap): void |
| `goodsType` | string([GoodsTypeEnum](http://localhost:3000/llms-pages/php/models/enumerations/goods-type.md)) | Required | This is a container for any-of cases. | getGoodsType(): string | setGoodsType(string goodsType): void |
| `items` | [`GuideItem[]`](http://localhost:3000/llms-pages/php/models/structures/guide-item.md) | Required | Items. | getItems(): array | setItems(array items): void |
| `modelRequested` | `bool` | Required | Model requested. | getModelRequested(): bool | setModelRequested(bool modelRequested): void |
| `modelTextShown` | `string` | Required, Constant | Model text shown.<br><br>**Value**: `'False'` | getModelTextShown(): string | setModelTextShown(string modelTextShown): void |
| `prefill` | `array<string,string>` | Required | Prefill. | getPrefill(): array | setPrefill(array prefill): void |
| `reply` | [GuideReply](http://localhost:3000/llms-pages/php/models/structures/guide-reply.md) | Required | This is a container for any-of cases. | getReply(): GuideReply | setReply(GuideReply reply): void |
| `review` | [`GuideReviewRow[]`](http://localhost:3000/llms-pages/php/models/structures/guide-review-row.md) | Required | Review. | getReview(): array | setReview(array review): void |
| `roundsUsed` | `int` | Required | Rounds used. | getRoundsUsed(): int | setRoundsUsed(int roundsUsed): void |
| `scenario` | string([Scenario1Enum](http://localhost:3000/llms-pages/php/models/enumerations/scenario-1.md)) | Required | This is a container for any-of cases. | getScenario(): string | setScenario(string scenario): void |
| `schemaVersion` | `int` | Required, Constant | Schema version.<br><br>**Value**: `1` | getSchemaVersion(): int | setSchemaVersion(int schemaVersion): void |
| `stage` | string([Stage3Enum](http://localhost:3000/llms-pages/php/models/enumerations/stage-3.md)) | Required | This is a container for any-of cases. | getStage(): string | setStage(string stage): void |
| `started` | `bool` | Required | Started. | getStarted(): bool | setStarted(bool started): void |
| `subtraction` | [GuideSubtraction](http://localhost:3000/llms-pages/php/models/structures/guide-subtraction.md) | Required | This is a container for any-of cases. | getSubtraction(): GuideSubtraction | setSubtraction(GuideSubtraction subtraction): void |
| `turnsLimit` | `int` | Required | Turns limit. | getTurnsLimit(): int | setTurnsLimit(int turnsLimit): void |
| `turnsUsed` | `int` | Required | Turns used. | getTurnsUsed(): int | setTurnsUsed(int turnsUsed): void |
| `valuesStored` | `string` | Required, Constant | Values stored.<br><br>**Value**: `'False'` | getValuesStored(): string | setValuesStored(string valuesStored): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\GuideStateResponseBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\GuideAnalysisBuilder;
use TradeGlotLocalConsoleLib\Models\Reason5Enum;
use TradeGlotLocalConsoleLib\Models\Status8Enum;
use TradeGlotLocalConsoleLib\Models\ChooserModeEnum;
use TradeGlotLocalConsoleLib\Models\Builders\GuideFormResultBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\GuideFieldResultBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\GuideGapBuilder;
use TradeGlotLocalConsoleLib\Models\GoodsTypeEnum;
use TradeGlotLocalConsoleLib\Models\Builders\GuideItemBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\GuideFormBuilder;
use TradeGlotLocalConsoleLib\Models\Kind2Enum;
use TradeGlotLocalConsoleLib\Models\Builders\GuideOptionBuilder;
use TradeGlotLocalConsoleLib\Models\Source8Enum;
use TradeGlotLocalConsoleLib\Models\Status9Enum;
use TradeGlotLocalConsoleLib\Models\Builders\GuideReplyBuilder;
use TradeGlotLocalConsoleLib\Models\ChooserEnum;
use TradeGlotLocalConsoleLib\Models\Builders\GuideDroppedBuilder;
use TradeGlotLocalConsoleLib\Models\Reason6Enum;
use TradeGlotLocalConsoleLib\Models\FallbackReasonEnum;
use TradeGlotLocalConsoleLib\Models\TemplateEnum;
use TradeGlotLocalConsoleLib\Models\Builders\GuideReviewRowBuilder;
use TradeGlotLocalConsoleLib\Models\Source9Enum;
use TradeGlotLocalConsoleLib\Models\Scenario1Enum;
use TradeGlotLocalConsoleLib\Models\Stage3Enum;
use TradeGlotLocalConsoleLib\Models\Builders\GuideSubtractionBuilder;

$guideStateResponse = GuideStateResponseBuilder::init(
    GuideAnalysisBuilder::init(
        Reason5Enum::INVALID_REPLY,
        Status8Enum::REPLACED,
        186
    )->build(),
    [
        'asked6',
        'asked7'
    ],
    [
        'auto_confirmed2',
        'auto_confirmed3'
    ],
    ChooserModeEnum::KEYWORD,
    [
        'deferred9'
    ],
    'String1',
    GuideFormResultBuilder::init(
        'item2',
        false
    )->build(),
    [
        GuideFieldResultBuilder::init(
            false,
            'item6',
            false
        )->build()
    ],
    GuideGapBuilder::init(
        [
            'conflicting9',
            'conflicting8'
        ],
        [
            'missing2',
            'missing3',
            'missing4'
        ],
        [
            'partial4',
            'partial3',
            'partial2'
        ],
        [
            'present7',
            'present8'
        ]
    )->build(),
    GoodsTypeEnum::PHYSICAL,
    [
        GuideItemBuilder::init(
            'String9',
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
            'id8',
            'label8',
            Source8Enum::OFFICIAL,
            Status9Enum::MISSING
        )->build()
    ],
    false,
    [
        'key0' => 'prefill7',
        'key1' => 'prefill8',
        'key2' => 'prefill9'
    ],
    GuideReplyBuilder::init(
        ChooserEnum::FORM,
        [
            GuideDroppedBuilder::init(
                'item2',
                Reason6Enum::OTHER_PARTY
            )->build()
        ],
        FallbackReasonEnum::LATE,
        false,
        TemplateEnum::REVIEW,
        'text0'
    )->build(),
    [
        GuideReviewRowBuilder::init(
            'item4',
            Source9Enum::WORDS,
            'value4'
        )->build()
    ],
    242,
    Scenario1Enum::DISPUTE,
    Stage3Enum::REVIEW,
    false,
    GuideSubtractionBuilder::init(
        64,
        190,
        178,
        'text0'
    )->build(),
    230,
    128
)->build();
```



