# Finding

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRkZpbmRpbmc

Finding.


# Class Name

`Finding`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `category` | [`CategoryEnum`](http://localhost:3000/llms-pages/ruby/models/enumerations/category.md) | Required | Category. |
| `code` | `String` | Required, Constant | Code.<br><br>**Value**: `'keyword_requires_policy_review'` |


# Example

```ruby
finding = Finding.new(
  CategoryEnum::UNSUPPORTED_FINANCIAL_PROMISE,
  'keyword_requires_policy_review'
)
```



