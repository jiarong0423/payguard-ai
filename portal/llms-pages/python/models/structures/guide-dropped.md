# Guide Dropped

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRkd1aWRlRHJvcHBlZA

GuideDropped.


# Class Name

`GuideDropped`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `item` | `str` | Required | Item. |
| `reason` | [`Reason6Enum`](http://localhost:3000/llms-pages/python/models/enumerations/reason-6.md) | Required | Reason. |


# Example

```python
from tradeglotlocalconsole.models.guide_dropped import GuideDropped
from tradeglotlocalconsole.models.reason_6_enum import Reason6Enum

guide_dropped = GuideDropped(
    item='item6',
    reason=Reason6Enum.OTHER_PARTY
)
```



