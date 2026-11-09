# Form

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkZvcm0

Form.


# Class Name

`Form`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `kind` | [`Kind2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/kind-2.md) | Optional | Kind. |
| `options` | [`Array[GuideOption]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/guide-option.md) | Optional | Options. |
| `placeholder` | String \| nil | Optional | This is a container for any-of cases. |


# Example

```ruby
form = Form.new(
  Kind2Enum::TEXT,
  [
    GuideOption.new(
      'label2',
      'value4'
    ),
    GuideOption.new(
      'label2',
      'value4'
    ),
    GuideOption.new(
      'label2',
      'value4'
    )
  ],
  'String9'
)
```



