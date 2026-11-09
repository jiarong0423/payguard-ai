# Identity Tokens

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRklkZW50aXR5VG9rZW5z

IdentityTokens.


# Class Name

`IdentityTokens`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AddressToken` | `string` | Required | Address token. |
| `EmailToken` | `string` | Required | Email token. |
| `NameToken` | `string` | Required | Name token. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    identityTokens := models.IdentityTokens{
        AddressToken: "address_token6",
        EmailToken:   "email_token8",
        NameToken:    "name_token4",
    }

}
```



