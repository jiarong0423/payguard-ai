# Provider Money

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRlByb3ZpZGVyTW9uZXk

ProviderMoney.


# Class Name

`ProviderMoney`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `currency_code` | `String` | Required | Currency code.<br><br>**Constraints**: *Pattern*: `^[A-Z]{3}$` |
| `value` | `String` | Required | Value.<br><br>**Constraints**: *Pattern*: `^[0-9]{1,10}(?:\.[0-9]{1,2})?$` |


# Example

```ruby
provider_money = ProviderMoney.new(
  'currency_code8',
  'value4'
)
```



