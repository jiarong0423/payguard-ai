# Time Evidence

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRlRpbWVFdmlkZW5jZQ

TimeEvidence.


# Class Name

`TimeEvidence`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `advisoryOnly` | `string` | Required, Constant | Advisory only.<br><br>**Value**: `'True'` | getAdvisoryOnly(): string | setAdvisoryOnly(string advisoryOnly): void |
| `events` | array<[Message[TimeEvent](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/time-event.md)]($m/Message[TimeEvent]($m/TimeEvent))\|[TimeEvent](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/time-event.md)> | Required | This is Array of a container for any-of cases.<br><br>**Constraints**: *Minimum Items*: `2`, *Maximum Items*: `30` | getEvents(): array | setEvents(array events): void |
| `flags` | [`string(FlagEnum)[]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/flag.md) | Required | Flags.<br><br>**Constraints**: *Maximum Items*: `4` | getFlags(): array | setFlags(array flags): void |
| `gapsSeconds` | [`TimeGaps`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/time-gaps.md) | Required | TimeGaps. | getGapsSeconds(): TimeGaps | setGapsSeconds(TimeGaps gapsSeconds): void |
| `judgement` | `string` | Required, Constant | Judgement.<br><br>**Value**: `'NOT_MADE'` | getJudgement(): string | setJudgement(string judgement): void |
| `schemaVersion` | `string` | Required, Constant | Schema version.<br><br>**Value**: `'payguard.time_evidence.v1'` | getSchemaVersion(): string | setSchemaVersion(string schemaVersion): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\TimeEvidenceBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\MessageTimeEventBuilder;
use TradeGlotLocalConsoleLib\Models\ChannelEnum;
use TradeGlotLocalConsoleLib\Models\DirectionEnum;
use TradeGlotLocalConsoleLib\Models\TopicEnum;
use TradeGlotLocalConsoleLib\Models\FlagEnum;
use TradeGlotLocalConsoleLib\Models\Builders\TimeGapsBuilder;

$timeEvidence = TimeEvidenceBuilder::init(
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
        )->build(),
        MessageTimeEventBuilder::init(
            'at4',
            ChannelEnum::EMAIL,
            DirectionEnum::INBOUND,
            'message_digest2',
            TopicEnum::ORDER_DETAILS_PROVIDED
        )->build()
    ],
    [
        FlagEnum::DELIVERY_AFTER_CLAIM,
        FlagEnum::CLAIM_TIME_EARLIER_THAN_PAYMENT_TIME
    ],
    TimeGapsBuilder::init(
        210,
        154,
        192,
        208
    )->build()
)->build();
```



