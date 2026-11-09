# Identity Redaction

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRklkZW50aXR5UmVkYWN0aW9u

IdentityRedaction.


# Class Name

`IdentityRedaction`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `fields` | [`string(FieldEnum)[]`](http://localhost:3000/llms-pages/php/models/enumerations/field.md) | Required | Fields. | getFields(): array | setFields(array fields): void |
| `method` | `string` | Required, Constant | Method.<br><br>**Value**: `'HMAC-SHA256 pseudonymization'` | getMethod(): string | setMethod(string method): void |
| `synthetic` | `string` | Required, Constant | Synthetic.<br><br>**Value**: `'True'` | getSynthetic(): string | setSynthetic(string synthetic): void |
| `tokens` | [`IdentityTokens`](http://localhost:3000/llms-pages/php/models/structures/identity-tokens.md) | Required | IdentityTokens. | getTokens(): IdentityTokens | setTokens(IdentityTokens tokens): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\IdentityRedactionBuilder;
use TradeGlotLocalConsoleLib\Models\FieldEnum;
use TradeGlotLocalConsoleLib\Models\Builders\IdentityTokensBuilder;

$identityRedaction = IdentityRedactionBuilder::init(
    [
        FieldEnum::NAME,
        FieldEnum::ADDRESS
    ],
    IdentityTokensBuilder::init(
        'address_token0',
        'email_token2',
        'name_token0'
    )->build()
)->build();
```



