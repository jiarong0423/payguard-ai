# Guide Dropped

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkd1aWRlRHJvcHBlZA

GuideDropped.


# Class Name

`GuideDropped`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `item` | `str` | Required | Item. |
| `reason` | [`Reason6Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/reason-6.md) | Required | Reason. |


# Example

```python
from tradeglotlocalconsole.models.guide_dropped import GuideDropped
from tradeglotlocalconsole.models.reason_6_enum import Reason6Enum

guide_dropped = GuideDropped(
    item='item6',
    reason=Reason6Enum.OTHER_PARTY
)
```



