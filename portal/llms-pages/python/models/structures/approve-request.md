# Approve Request

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRkFwcHJvdmVSZXF1ZXN0

ApproveRequest.


# Class Name

`ApproveRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `draft_digest` | `str` | Required | Draft digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |


# Example

```python
from tradeglotlocalconsole.models.approve_request import ApproveRequest

approve_request = ApproveRequest(
    draft_digest='draft_digest6'
)
```



