# Identity Redaction

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRklkZW50aXR5UmVkYWN0aW9u

IdentityRedaction.


# Class Name

`IdentityRedaction`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `fields` | [`Array[FieldEnum]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/field.md) | Required | Fields. |
| `method` | `String` | Required, Constant | Method.<br><br>**Value**: `'HMAC-SHA256 pseudonymization'` |
| `synthetic` | `String` | Required, Constant | Synthetic.<br><br>**Value**: `'True'` |
| `tokens` | [`IdentityTokens`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/identity-tokens.md) | Required | IdentityTokens. |


# Example

```ruby
identity_redaction = IdentityRedaction.new(
  [
    FieldEnum::ADDRESS,
    FieldEnum::EMAIL,
    FieldEnum::NAME
  ],
  'HMAC-SHA256 pseudonymization',
  'True',
  IdentityTokens.new(
    'address_token0',
    'email_token2',
    'name_token0'
  )
)
```



