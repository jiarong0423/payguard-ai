# Time Evidence 1

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRlRpbWVFdmlkZW5jZTE

Time evidence.


# Class Name

`TimeEvidence1`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `advisoryOnly` | `?bool` | Optional | Advisory only. | getAdvisoryOnly(): ?bool | setAdvisoryOnly(?bool advisoryOnly): void |
| `events` | array<[Message[TimeEvent](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/time-event.md)]($m/Message[TimeEvent]($m/TimeEvent))\|[TimeEvent](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/time-event.md)>\|null | Optional | This is Array of a container for any-of cases.<br><br>**Constraints**: *Minimum Items*: `2`, *Maximum Items*: `30` | getEvents(): ?array | setEvents(?array events): void |
| `flags` | [`?(string(FlagEnum)[])`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/flag.md) | Optional | Flags.<br><br>**Constraints**: *Maximum Items*: `4` | getFlags(): ?array | setFlags(?array flags): void |
| `gapsSeconds` | [`?TimeGaps`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/time-gaps.md) | Optional | TimeGaps. | getGapsSeconds(): ?TimeGaps | setGapsSeconds(?TimeGaps gapsSeconds): void |
| `judgement` | [`?string(JudgementEnum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/judgement.md) | Optional | Judgement. | getJudgement(): ?string | setJudgement(?string judgement): void |
| `schemaVersion` | [`?string(SchemaVersionEnum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/schema-version.md) | Optional | Schema version. | getSchemaVersion(): ?string | setSchemaVersion(?string schemaVersion): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\TimeEvidence1Builder;
use TradeGlotLocalConsoleLib\Models\Builders\MessageTimeEventBuilder;
use TradeGlotLocalConsoleLib\Models\ChannelEnum;
use TradeGlotLocalConsoleLib\Models\DirectionEnum;
use TradeGlotLocalConsoleLib\Models\TopicEnum;
use TradeGlotLocalConsoleLib\Models\FlagEnum;
use TradeGlotLocalConsoleLib\Models\Builders\TimeGapsBuilder;
use TradeGlotLocalConsoleLib\Models\JudgementEnum;

$timeEvidence1 = TimeEvidence1Builder::init()
    ->advisoryOnly(false)
    ->events(
        [
            MessageTimeEventBuilder::init(
                'at4',
                ChannelEnum::EMAIL,
                DirectionEnum::INBOUND,
                'message_digest2',
                TopicEnum::ORDER_DETAILS_PROVIDED
            )->build(),
            MessageTimeEventBuilder::init(
                'at4',
                ChannelEnum::EMAIL,
                DirectionEnum::INBOUND,
                'message_digest2',
                TopicEnum::ORDER_DETAILS_PROVIDED
            )->build()
        ]
    )
    ->flags(
        [
            FlagEnum::ORDER_RECORD_ABSENT,
            FlagEnum::DELIVERY_NOT_RECORDED
        ]
    )
    ->gapsSeconds(
        TimeGapsBuilder::init(
            210,
            154,
            192,
            208
        )->build()
    )
    ->judgement(JudgementEnum::NOT_MADE)
    ->build();
```



