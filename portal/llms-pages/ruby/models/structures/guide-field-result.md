# Guide Field Result

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkd1aWRlRmllbGRSZXN1bHQ

GuideFieldResult.


# Class Name

`GuideFieldResult`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `deferred` | `TrueClass \| FalseClass` | Required | Deferred. |
| `item` | `String` | Required | Item. |
| `valid` | `TrueClass \| FalseClass` | Required | Valid. |


# Example

```ruby
guide_field_result = GuideFieldResult.new(
  false,
  'item8',
  false
)
```



