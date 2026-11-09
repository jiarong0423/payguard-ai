# Identity Redaction

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRklkZW50aXR5UmVkYWN0aW9u

IdentityRedaction.


# Class Name

`IdentityRedaction`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Fields` | [`[]models.FieldEnum`](http://localhost:3000/llms-pages/go/models/enumerations/field.md) | Required | Fields. |
| `Method` | `string` | Required, Constant | Method.<br><br>**Value**: `"HMAC-SHA256 pseudonymization"` |
| `Synthetic` | `string` | Required, Constant | Synthetic.<br><br>**Value**: `"True"` |
| `Tokens` | [`models.IdentityTokens`](http://localhost:3000/llms-pages/go/models/structures/identity-tokens.md) | Required | IdentityTokens. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    identityRedaction := models.IdentityRedaction{
        Fields:    []models.FieldEnum{
            models.FieldEnum_NAME,
            models.FieldEnum_ADDRESS,
        },
        Method:    "HMAC-SHA256 pseudonymization",
        Synthetic: "True",
        Tokens:    models.IdentityTokens{
            AddressToken: "address_token0",
            EmailToken:   "email_token2",
            NameToken:    "name_token0",
        },
    }

}
```



