# Identity Redaction

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0bSUyRklkZW50aXR5UmVkYWN0aW9u

IdentityRedaction.


# Interface Name

`IdentityRedaction`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `fields` | [`FieldEnum[]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/enumerations/field.md) | Required | Fields. |
| `method` | `string` | Required, Constant | Method.<br><br>**Value**: `'HMAC-SHA256 pseudonymization'` |
| `synthetic` | `string` | Required, Constant | Synthetic.<br><br>**Value**: `'True'` |
| `tokens` | [`IdentityTokens`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/identity-tokens.md) | Required | IdentityTokens. |


# Example

```ts
import { FieldEnum, IdentityRedaction } from 'tradeglot-local-consolelib';

const identityRedaction: IdentityRedaction = {
  fields: [
    FieldEnum.Name,
    FieldEnum.Address
  ],
  method: 'HMAC-SHA256 pseudonymization',
  synthetic: 'True',
  tokens: {
    addressToken: 'address_token0',
    emailToken: 'email_token2',
    nameToken: 'name_token0',
  },
};
```



