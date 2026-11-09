# Error

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkVycm9y

What was refused and why.


# Class Name

`Error`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `code` | `str` | Required | Stable machine-readable reason, for example session_required. |
| `message` | `str` | Required | A plain sentence for a person. |


# Example

```python
from tradeglotlocalconsole.models.error import Error

error = Error(
    code='code2',
    message='message4'
)
```



