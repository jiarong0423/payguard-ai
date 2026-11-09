# Identity Tokens

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRklkZW50aXR5VG9rZW5z

IdentityTokens.


# Class Name

`IdentityTokens`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `address_token` | `String` | Required | Address token. |
| `email_token` | `String` | Required | Email token. |
| `name_token` | `String` | Required | Name token. |


# Example

```ruby
identity_tokens = IdentityTokens.new(
  'address_token0',
  'email_token2',
  'name_token0'
)
```



