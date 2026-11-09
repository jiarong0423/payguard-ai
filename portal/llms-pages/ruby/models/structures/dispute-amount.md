# Dispute Amount

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkRpc3B1dGVBbW91bnQ

Dispute amount.


# Class Name

`DisputeAmount`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `currency_code` | `String` | Optional | Currency code.<br><br>**Constraints**: *Pattern*: `^[A-Z]{3}$` |
| `value` | `String` | Optional | Value.<br><br>**Constraints**: *Pattern*: `^[0-9]{1,10}(?:\.[0-9]{1,2})?$` |


# Example

```ruby
dispute_amount = DisputeAmount.new(
  'currency_code6',
  'value0'
)
```



