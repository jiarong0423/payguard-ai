# Identity Redaction

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRklkZW50aXR5UmVkYWN0aW9u

IdentityRedaction.


# Class Name

`IdentityRedaction`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Fields` | [`List<FieldEnum>`](http://localhost:3000/llms-pages/net-standard-library/models/enumerations/field.md) | Required | Fields. |
| `Method` | `string` | Required, Constant | Method.<br><br>**Value**: `"HMAC-SHA256 pseudonymization"` |
| `Synthetic` | `string` | Required, Constant | Synthetic.<br><br>**Value**: `"True"` |
| `Tokens` | [`IdentityTokens`](http://localhost:3000/llms-pages/net-standard-library/models/structures/identity-tokens.md) | Required | IdentityTokens. |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;

IdentityRedaction identityRedaction = new IdentityRedaction
{
    Fields = new List<FieldEnum>
    {
        FieldEnum.Name,
        FieldEnum.Address,
    },
    Method = "HMAC-SHA256 pseudonymization",
    Synthetic = "True",
    Tokens = new IdentityTokens
    {
        AddressToken = "address_token0",
        EmailToken = "email_token2",
        NameToken = "name_token0",
    },
};
```



