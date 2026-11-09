# Inject Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkluamVjdFJlcXVlc3Q

InjectRequest.


# Class Name

`InjectRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `scenario` | [`Scenario5Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/scenario-5.md) | Required | Scenario. |


# Example

```python
from tradeglotlocalconsole.models.inject_request import InjectRequest
from tradeglotlocalconsole.models.scenario_5_enum import Scenario5Enum

inject_request = InjectRequest(
    scenario=Scenario5Enum.BURST
)
```



