# Identity Tokens

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRklkZW50aXR5VG9rZW5z

IdentityTokens.


# Class Name

`IdentityTokens`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `AddressToken` | `String` | Required | Address token. | String getAddressToken() | setAddressToken(String addressToken) |
| `EmailToken` | `String` | Required | Email token. | String getEmailToken() | setEmailToken(String emailToken) |
| `NameToken` | `String` | Required | Name token. | String getNameToken() | setNameToken(String nameToken) |


# Example

```java
import m18000.m0.m0.m127.models.IdentityTokens;

IdentityTokens identityTokens = new IdentityTokens.Builder(
    "address_token6",
    "email_token8",
    "name_token4"
)
.build();
```



