# Identity Tokens

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRklkZW50aXR5VG9rZW5z

IdentityTokens.


# Class Name

`IdentityTokens`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `address_token` | `str` | Required | Address token. |
| `email_token` | `str` | Required | Email token. |
| `name_token` | `str` | Required | Name token. |


# Example

```python
from tradeglotlocalconsole.models.identity_tokens import IdentityTokens

identity_tokens = IdentityTokens(
    address_token='address_token0',
    email_token='email_token2',
    name_token='name_token0'
)
```



