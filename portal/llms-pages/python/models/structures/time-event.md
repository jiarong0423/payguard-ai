# Time Event

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRlRpbWVFdmVudA

TimeEvent.


# Class Name

`TimeEvent`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `at` | `str` | Required | At.<br><br>**Constraints**: *Minimum Length*: `20`, *Maximum Length*: `40` |
| `kind` | [`KindEnum`](http://localhost:3000/llms-pages/python/models/enumerations/kind.md) | Required | Kind. |
| `source` | [`Source5Enum`](http://localhost:3000/llms-pages/python/models/enumerations/source-5.md) | Required | Source. |


# Example

```python
from tradeglotlocalconsole.models.kind_enum import KindEnum
from tradeglotlocalconsole.models.source_5_enum import Source5Enum
from tradeglotlocalconsole.models.time_event import TimeEvent

time_event = TimeEvent(
    at='at2',
    kind=KindEnum.PAYMENT,
    source=Source5Enum.PROVIDER
)
```



