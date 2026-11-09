# Session Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRlNlc3Npb25SZXNwb25zZQ

SessionResponse.


# Class Name

`SessionResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `csrf_token` | `str` | Required | Csrf token. |
| `expires_at` | `str` | Required | Expires at. |
| `session_id` | `str` | Required | Session id. |
| `source` | `str` | Required, Constant | Source.<br><br>**Value**: `"synthetic"` |


# Example

```python
from tradeglotlocalconsole.models.session_response import SessionResponse

session_response = SessionResponse(
    csrf_token='csrf_token8',
    expires_at='expires_at4',
    session_id='session_id2'
)
```



