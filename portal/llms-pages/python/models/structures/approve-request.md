# Approve Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkFwcHJvdmVSZXF1ZXN0

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



