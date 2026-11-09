# Disputed Transaction

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkRpc3B1dGVkVHJhbnNhY3Rpb24

DisputedTransaction.


# Class Name

`DisputedTransaction`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `gross_amount` | [ProviderMoney](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/provider-money.md) \| nil | Optional | This is a container for any-of cases. |
| `seller_protection_eligible` | TrueClass \| FalseClass \| nil | Optional | This is a container for any-of cases. |
| `seller_transaction_id` | `String` | Required | Seller transaction id.<br><br>**Constraints**: *Pattern*: `^[A-Za-z0-9._-]{1,64}$` |
| `transaction_status` | String \| nil | Optional | This is a container for any-of cases. |


# Example

```ruby
disputed_transaction = DisputedTransaction.new(
  'seller_transaction_id8',
  ProviderMoney.new(
    'currency_code0',
    'value6'
  ),
  true,
  'String3'
)
```



