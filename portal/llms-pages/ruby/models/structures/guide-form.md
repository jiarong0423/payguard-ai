# Guide Form

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkd1aWRlRm9ybQ

GuideForm.


# Class Name

`GuideForm`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `kind` | [`Kind2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/kind-2.md) | Required | Kind. |
| `options` | [`Array[GuideOption]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/guide-option.md) | Required | Options. |
| `placeholder` | String | Required | This is a container for any-of cases. |


# Example

```ruby
guide_form = GuideForm.new(
  Kind2Enum::TEXT,
  [
    GuideOption.new(
      'label2',
      'value4'
    )
  ],
  'String7'
)
```



