# Product Confirm Request

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRlByb2R1Y3RDb25maXJtUmVxdWVzdA

ProductConfirmRequest.


# Class Name

`ProductConfirmRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `description` | `String` | Required | Description.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `4000` |
| `evaluation_id` | `String` | Required | Evaluation id.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128`, *Pattern*: `^[A-Za-z0-9_-]+$` |
| `product_id` | String | Required | This is a container for any-of cases. |


# Example

```ruby
product_confirm_request = ProductConfirmRequest.new(
  'description4',
  'evaluation_id8',
  'String1'
)
```



