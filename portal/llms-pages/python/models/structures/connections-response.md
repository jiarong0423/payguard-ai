# Connections Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkNvbm5lY3Rpb25zUmVzcG9uc2U

Deployment mode only. Never a key, a key's presence, a value or a variable name.


# Class Name

`ConnectionsResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `mode` | [`ModeEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/mode.md) | Required | Mode. |
| `sandbox_reads` | bool \| None | Optional | This is a container for any-of cases. |


# Example

```python
from tradeglotlocalconsole.models.connections_response import ConnectionsResponse
from tradeglotlocalconsole.models.mode_enum import ModeEnum

connections_response = ConnectionsResponse(
    mode=ModeEnum.LOCAL,
    sandbox_reads=True
)
```



