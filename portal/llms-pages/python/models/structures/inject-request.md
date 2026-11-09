# Inject Request

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRkluamVjdFJlcXVlc3Q

InjectRequest.


# Class Name

`InjectRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `scenario` | [`Scenario5Enum`](http://localhost:3000/llms-pages/python/models/enumerations/scenario-5.md) | Required | Scenario. |


# Example

```python
from tradeglotlocalconsole.models.inject_request import InjectRequest
from tradeglotlocalconsole.models.scenario_5_enum import Scenario5Enum

inject_request = InjectRequest(
    scenario=Scenario5Enum.BURST
)
```



