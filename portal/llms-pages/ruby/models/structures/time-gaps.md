# Time Gaps

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRlRpbWVHYXBz

TimeGaps.


# Class Name

`TimeGaps`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `delivery_to_claim` | Integer | Required | This is a container for any-of cases. |
| `payment_to_claim` | Integer | Required | This is a container for any-of cases. |
| `payment_to_delivery` | Integer | Required | This is a container for any-of cases. |
| `payment_to_order_record` | Integer | Required | This is a container for any-of cases. |


# Example

```ruby
time_gaps = TimeGaps.new(
  88,
  20,
  30,
  74
)
```



