# Time Evidence

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRlRpbWVFdmlkZW5jZQ

TimeEvidence.


# Class Name

`TimeEvidence`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `advisory_only` | `str` | Required, Constant | Advisory only.<br><br>**Value**: `"True"` |
| `events` | List[[MessageTimeEvent](http://localhost:3000/llms-pages/python/models/structures/message-time-event.md) \| [TimeEvent](http://localhost:3000/llms-pages/python/models/structures/time-event.md)] | Required | This is List of a container for any-of cases.<br><br>**Constraints**: *Minimum Items*: `2`, *Maximum Items*: `30` |
| `flags` | [`List[FlagEnum]`](http://localhost:3000/llms-pages/python/models/enumerations/flag.md) | Required | Flags.<br><br>**Constraints**: *Maximum Items*: `4` |
| `gaps_seconds` | [`TimeGaps`](http://localhost:3000/llms-pages/python/models/structures/time-gaps.md) | Required | TimeGaps. |
| `judgement` | `str` | Required, Constant | Judgement.<br><br>**Value**: `"NOT_MADE"` |
| `schema_version` | `str` | Required, Constant | Schema version.<br><br>**Value**: `"payguard.time_evidence.v1"` |


# Example

```python
from tradeglotlocalconsole.models.channel_enum import ChannelEnum
from tradeglotlocalconsole.models.direction_enum import DirectionEnum
from tradeglotlocalconsole.models.flag_enum import FlagEnum
from tradeglotlocalconsole.models.message_time_event import MessageTimeEvent
from tradeglotlocalconsole.models.time_evidence import TimeEvidence
from tradeglotlocalconsole.models.time_gaps import TimeGaps
from tradeglotlocalconsole.models.topic_enum import TopicEnum

time_evidence = TimeEvidence(
    events=[
        MessageTimeEvent(
            at='at4',
            channel=ChannelEnum.EMAIL,
            direction=DirectionEnum.INBOUND,
            message_digest='message_digest2',
            topic=TopicEnum.ORDER_DETAILS_PROVIDED
        ),
        MessageTimeEvent(
            at='at4',
            channel=ChannelEnum.EMAIL,
            direction=DirectionEnum.INBOUND,
            message_digest='message_digest2',
            topic=TopicEnum.ORDER_DETAILS_PROVIDED
        ),
        MessageTimeEvent(
            at='at4',
            channel=ChannelEnum.EMAIL,
            direction=DirectionEnum.INBOUND,
            message_digest='message_digest2',
            topic=TopicEnum.ORDER_DETAILS_PROVIDED
        )
    ],
    flags=[
        FlagEnum.ORDER_RECORD_ABSENT
    ],
    gaps_seconds=TimeGaps(
        delivery_to_claim=210,
        payment_to_claim=154,
        payment_to_delivery=192,
        payment_to_order_record=208
    )
)
```



