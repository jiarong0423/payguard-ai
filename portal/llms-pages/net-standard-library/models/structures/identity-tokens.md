# Identity Tokens

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRklkZW50aXR5VG9rZW5z

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

```csharp
using TradeGlotLocalConsole.Standard.Models;

IdentityTokens identityTokens = new IdentityTokens
{
    AddressToken = "address_token6",
    EmailToken = "email_token8",
    NameToken = "name_token4",
};
```



