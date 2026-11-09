# Form

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRkZvcm0

Form.


# Class Name

`Form`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `kind` | [`Kind2Enum`](http://localhost:3000/llms-pages/ruby/models/enumerations/kind-2.md) | Optional | Kind. |
| `options` | [`Array[GuideOption]`](http://localhost:3000/llms-pages/ruby/models/structures/guide-option.md) | Optional | Options. |
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



