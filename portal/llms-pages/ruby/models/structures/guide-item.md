# Guide Item

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRkd1aWRlSXRlbQ

GuideItem.


# Class Name

`GuideItem`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `chunk` | String | Required | This is a container for any-of cases. |
| `form` | [GuideForm](http://localhost:3000/llms-pages/ruby/models/structures/guide-form.md) | Required | This is a container for any-of cases. |
| `id` | `String` | Required | Id. |
| `label` | `String` | Required | Label. |
| `source` | [`Source8Enum`](http://localhost:3000/llms-pages/ruby/models/enumerations/source-8.md) | Required | Source. |
| `status` | [`Status9Enum`](http://localhost:3000/llms-pages/ruby/models/enumerations/status-9.md) | Required | Status. |


# Example

```ruby
guide_item = GuideItem.new(
  'String1',
  GuideForm.new(
    Kind2Enum::CHOICE,
    [
      GuideOption.new(
        'label2',
        'value4'
      )
    ],
    'String9'
  ),
  'id6',
  'label6',
  Source8Enum::OFFICIAL,
  Status9Enum::STRUCTURALLY_PRESENT
)
```



