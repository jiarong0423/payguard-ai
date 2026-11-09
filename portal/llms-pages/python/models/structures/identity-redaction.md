# Identity Redaction

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRklkZW50aXR5UmVkYWN0aW9u

IdentityRedaction.


# Class Name

`IdentityRedaction`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `fields` | [`List[FieldEnum]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/field.md) | Required | Fields. |
| `method` | `str` | Required, Constant | Method.<br><br>**Value**: `"HMAC-SHA256 pseudonymization"` |
| `synthetic` | `str` | Required, Constant | Synthetic.<br><br>**Value**: `"True"` |
| `tokens` | [`IdentityTokens`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/identity-tokens.md) | Required | IdentityTokens. |


# Example

```python
from tradeglotlocalconsole.models.field_enum import FieldEnum
from tradeglotlocalconsole.models.identity_redaction import IdentityRedaction
from tradeglotlocalconsole.models.identity_tokens import IdentityTokens

identity_redaction = IdentityRedaction(
    fields=[
        FieldEnum.ADDRESS,
        FieldEnum.EMAIL,
        FieldEnum.NAME
    ],
    tokens=IdentityTokens(
        address_token='address_token0',
        email_token='email_token2',
        name_token='name_token0'
    )
)
```



