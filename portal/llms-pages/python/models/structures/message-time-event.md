# Message Time Event

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRk1lc3NhZ2VUaW1lRXZlbnQ

MessageTimeEvent.


# Class Name

`MessageTimeEvent`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `at` | `str` | Required | At.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `40` |
| `channel` | [`ChannelEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/channel.md) | Required | Channel. |
| `direction` | [`DirectionEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/direction.md) | Required | Direction. |
| `kind` | `str` | Required, Constant | Kind.<br><br>**Value**: `"MESSAGE"` |
| `message_digest` | `str` | Required | Message digest.<br><br>**Constraints**: *Pattern*: `^[0-9a-f]{64}$` |
| `source` | `str` | Required, Constant | Source.<br><br>**Value**: `"SELLER_PROVIDED_UNVERIFIED"` |
| `topic` | [`TopicEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/topic.md) | Required | Topic. |


# Example

```python
from tradeglotlocalconsole.models.channel_enum import ChannelEnum
from tradeglotlocalconsole.models.direction_enum import DirectionEnum
from tradeglotlocalconsole.models.message_time_event import MessageTimeEvent
from tradeglotlocalconsole.models.topic_enum import TopicEnum

message_time_event = MessageTimeEvent(
    at='at2',
    channel=ChannelEnum.EMAIL,
    direction=DirectionEnum.INBOUND,
    message_digest='message_digest0',
    topic=TopicEnum.ORDER_DETAILS_PROVIDED
)
```



