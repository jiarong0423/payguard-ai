# Guide Analysis

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRkd1aWRlQW5hbHlzaXM

GuideAnalysis.


# Class Name

`GuideAnalysis`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `reason` | [Reason5](http://localhost:3000/llms-pages/python/models/enumerations/reason-5.md) | Required | This is a container for any-of cases. |
| `status` | [`Status8Enum`](http://localhost:3000/llms-pages/python/models/enumerations/status-8.md) | Required | Status. |
| `turn` | `int` | Required | Turn. |


# Example

```python
from tradeglotlocalconsole.models.guide_analysis import GuideAnalysis
from tradeglotlocalconsole.models.reason_5_enum import Reason5Enum
from tradeglotlocalconsole.models.status_8_enum import Status8Enum

guide_analysis = GuideAnalysis(
    reason=Reason5Enum.BUDGET,
    status=Status8Enum.REPLACED,
    turn=142
)
```



