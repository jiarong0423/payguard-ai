# Guide Form Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkd1aWRlRm9ybVJlcXVlc3Q

One field ({item, value}) or one round of up to three fields ({fields: [...]}), never both.


# Class Name

`GuideFormRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `confirm_review` | `TrueClass \| FalseClass` | Optional | Confirm review.<br><br>**Default**: `false` |
| `fields` | Array[[GuideField](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/guide-field.md)] \| nil | Optional | This is a container for any-of cases. |
| `item` | String \| nil | Optional | This is a container for any-of cases. |
| `scenario` | [Scenario1](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/scenario-1.md) \| nil | Optional | This is a container for any-of cases. |
| `value` | String \| nil | Optional | This is a container for any-of cases. |


# Example

```ruby
guide_form_request = GuideFormRequest.new(
  false,
  [
    GuideField.new(
      'item8',
      'value8'
    )
  ],
  'String9',
  Scenario1Enum::PREFLIGHT,
  'String9'
)
```



