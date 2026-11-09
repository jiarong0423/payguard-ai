# Guide Dropped

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRkd1aWRlRHJvcHBlZA

GuideDropped.


# Class Name

`GuideDropped`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `item` | `String` | Required | Item. |
| `reason` | [`Reason6Enum`](http://localhost:3000/llms-pages/ruby/models/enumerations/reason-6.md) | Required | Reason. |


# Example

```ruby
guide_dropped = GuideDropped.new(
  'item6',
  Reason6Enum::OTHER_PARTY
)
```



