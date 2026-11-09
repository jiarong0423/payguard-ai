# Identity Tokens

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRklkZW50aXR5VG9rZW5z

IdentityTokens.


# Class Name

`IdentityTokens`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `addressToken` | `string` | Required | Address token. | getAddressToken(): string | setAddressToken(string addressToken): void |
| `emailToken` | `string` | Required | Email token. | getEmailToken(): string | setEmailToken(string emailToken): void |
| `nameToken` | `string` | Required | Name token. | getNameToken(): string | setNameToken(string nameToken): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\IdentityTokensBuilder;

$identityTokens = IdentityTokensBuilder::init(
    'address_token6',
    'email_token8',
    'name_token4'
)->build();
```



