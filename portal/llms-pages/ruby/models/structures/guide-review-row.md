# Guide Review Row

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkd1aWRlUmV2aWV3Um93

GuideReviewRow.


# Class Name

`GuideReviewRow`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `item` | `String` | Required | Item. |
| `source` | [`Source9Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/source-9.md) | Required | Source. |
| `value` | `String` | Required | Value.<br><br>**Constraints**: *Maximum Length*: `120` |


# Example

```ruby
guide_review_row = GuideReviewRow.new(
  'item2',
  Source9Enum::WORDS,
  'value2'
)
```



