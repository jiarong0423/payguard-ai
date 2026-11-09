# Guide Review Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkd1aWRlUmV2aWV3UmVxdWVzdA

GuideReviewRequest.


# Class Name

`GuideReviewRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `change` | `Array[String]` | Optional | Change.<br><br>**Constraints**: *Maximum Items*: `9`, *Minimum Length*: `1`, *Maximum Length*: `40`, *Pattern*: `^[a-z_]+$` |
| `confirm` | `TrueClass \| FalseClass` | Optional | Confirm.<br><br>**Default**: `false` |
| `scenario` | [Scenario1](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/scenario-1.md) \| nil | Optional | This is a container for any-of cases. |


# Example

```ruby
guide_review_request = GuideReviewRequest.new(
  [
    'change1',
    'change2'
  ],
  false,
  Scenario1Enum::VELOCITY
)
```



