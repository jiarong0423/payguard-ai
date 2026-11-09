# Health Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkhlYWx0aFJlc3BvbnNl

HealthResponse.


# Class Name

`HealthResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `mode` | `str` | Required, Constant | Mode.<br><br>**Value**: `"demo"` |
| `source` | `str` | Required, Constant | Source.<br><br>**Value**: `"synthetic"` |
| `status` | `str` | Required, Constant | Status.<br><br>**Value**: `"ok"` |
| `version` | `str` | Required | Version. |


# Example

```python
from tradeglotlocalconsole.models.health_response import HealthResponse

health_response = HealthResponse(
    version='version2'
)
```



