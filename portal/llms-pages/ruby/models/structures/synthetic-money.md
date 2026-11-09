# Synthetic Money

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRlN5bnRoZXRpY01vbmV5

Same shape as the PayPal Disputes `dispute_amount` (ProviderMoney below); values are synthetic.


# Class Name

`SyntheticMoney`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `currency_code` | `String` | Required | Currency code.<br><br>**Constraints**: *Pattern*: `^[A-Z]{3}$` |
| `value` | `String` | Required | Value.<br><br>**Constraints**: *Pattern*: `^[0-9]{1,10}(?:\.[0-9]{1,2})?$` |


# Example

```ruby
synthetic_money = SyntheticMoney.new(
  'currency_code8',
  'value4'
)
```



