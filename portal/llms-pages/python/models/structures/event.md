# Event

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRkV2ZW50


# Class Name

`Event`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `at` | `str` | Optional | At.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `40` |
| `channel` | [`ChannelEnum`](http://localhost:3000/llms-pages/python/models/enumerations/channel.md) | Optional | Channel. |
| `direction` | [`DirectionEnum`](http://localhost:3000/llms-pages/python/models/enumerations/direction.md) | Optional | Direction. |
| `kind` | [`Kind1Enum`](http://localhost:3000/llms-pages/python/models/enumerations/kind-1.md) | Optional | Kind. |
| `message_digest` | `str` | Optional | Message digest.<br><br>**Constraints**: *Pattern*: `^[0-9a-f]{64}$` |
| `source` | [`Source6Enum`](http://localhost:3000/llms-pages/python/models/enumerations/source-6.md) | Optional | Source. |
| `topic` | [`TopicEnum`](http://localhost:3000/llms-pages/python/models/enumerations/topic.md) | Optional | Topic. |


# Example

```python
from tradeglotlocalconsole.models.channel_enum import ChannelEnum
from tradeglotlocalconsole.models.direction_enum import DirectionEnum
from tradeglotlocalconsole.models.event import Event
from tradeglotlocalconsole.models.kind_1_enum import Kind1Enum

event = Event(
    at='at6',
    channel=ChannelEnum.EMAIL,
    direction=DirectionEnum.INBOUND,
    kind=Kind1Enum.MESSAGE,
    message_digest='message_digest6'
)
```



