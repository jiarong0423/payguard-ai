# Analysis

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkFuYWx5c2lz

Analysis.


# Class Name

`Analysis`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `reason` | [Reason5](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/reason-5.md) \| None | Optional | This is a container for any-of cases. |
| `status` | [`Status8Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/status-8.md) | Optional | Status. |
| `turn` | `int` | Optional | Turn. |


# Example

```python
from tradeglotlocalconsole.models.analysis import Analysis
from tradeglotlocalconsole.models.reason_5_enum import Reason5Enum
from tradeglotlocalconsole.models.status_8_enum import Status8Enum

analysis = Analysis(
    reason=Reason5Enum.INVALID_REPLY,
    status=Status8Enum.REPLACED,
    turn=198
)
```



