# Guide Turn Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkd1aWRlVHVyblJlcXVlc3Q

GuideTurnRequest.


# Class Name

`GuideTurnRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `fields` | Array[[GuideField](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/guide-field.md)] \| nil | Optional | This is a container for any-of cases. |
| `scenario` | [Scenario1](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/scenario-1.md) \| nil | Optional | This is a container for any-of cases. |
| `text` | `String` | Required | Text.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `1600` |


# Example

```ruby
guide_turn_request = GuideTurnRequest.new(
  'text0',
  [
    GuideField.new(
      'item8',
      'value8'
    ),
    GuideField.new(
      'item8',
      'value8'
    ),
    GuideField.new(
      'item8',
      'value8'
    )
  ],
  Scenario1Enum::DISPUTE
)
```



