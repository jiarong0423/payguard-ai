# Time Evidence 1

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRlRpbWVFdmlkZW5jZTE

Time evidence.


# Class Name

`TimeEvidence1`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `advisory_only` | `bool` | Optional | Advisory only. |
| `events` | List[[MessageTimeEvent](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/message-time-event.md) \| [TimeEvent](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/time-event.md)] \| None | Optional | This is List of a container for any-of cases.<br><br>**Constraints**: *Minimum Items*: `2`, *Maximum Items*: `30` |
| `flags` | [`List[FlagEnum]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/flag.md) | Optional | Flags.<br><br>**Constraints**: *Maximum Items*: `4` |
| `gaps_seconds` | [`TimeGaps`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/time-gaps.md) | Optional | TimeGaps. |
| `judgement` | [`JudgementEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/judgement.md) | Optional | Judgement. |
| `schema_version` | [`SchemaVersionEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/schema-version.md) | Optional | Schema version. |


# Example

```python
from tradeglotlocalconsole.models.channel_enum import ChannelEnum
from tradeglotlocalconsole.models.direction_enum import DirectionEnum
from tradeglotlocalconsole.models.flag_enum import FlagEnum
from tradeglotlocalconsole.models.judgement_enum import JudgementEnum
from tradeglotlocalconsole.models.message_time_event import MessageTimeEvent
from tradeglotlocalconsole.models.time_evidence_1 import TimeEvidence1
from tradeglotlocalconsole.models.time_gaps import TimeGaps
from tradeglotlocalconsole.models.topic_enum import TopicEnum

time_evidence_1 = TimeEvidence1(
    advisory_only=False,
    events=[
        MessageTimeEvent(
            at='at4',
            channel=ChannelEnum.EMAIL,
            direction=DirectionEnum.INBOUND,
            message_digest='message_digest2',
            topic=TopicEnum.ORDER_DETAILS_PROVIDED
        )
    ],
    flags=[
        FlagEnum.ORDER_RECORD_ABSENT,
        FlagEnum.DELIVERY_NOT_RECORDED,
        FlagEnum.DELIVERY_AFTER_CLAIM
    ],
    gaps_seconds=TimeGaps(
        delivery_to_claim=210,
        payment_to_claim=154,
        payment_to_delivery=192,
        payment_to_order_record=208
    ),
    judgement=JudgementEnum.NOT_MADE
)
```



