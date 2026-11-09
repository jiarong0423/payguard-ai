# Reply

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRlJlcGx5

Reply.


# Class Name

`Reply`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `chooser` | [`ChooserEnum`](http://localhost:3000/llms-pages/ruby/models/enumerations/chooser.md) | Optional | Chooser. |
| `dropped` | [`Array[GuideDropped]`](http://localhost:3000/llms-pages/ruby/models/structures/guide-dropped.md) | Optional | Dropped. |
| `fallback_reason` | [FallbackReason](http://localhost:3000/llms-pages/ruby/models/enumerations/fallback-reason.md) \| nil | Optional | This is a container for any-of cases. |
| `state_changed` | `TrueClass \| FalseClass` | Optional | State changed. |
| `template` | [`TemplateEnum`](http://localhost:3000/llms-pages/ruby/models/enumerations/template.md) | Optional | Template. |
| `text` | `String` | Optional | Text.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `400` |


# Example

```ruby
reply = Reply.new(
  ChooserEnum::KEYWORD,
  [
    GuideDropped.new(
      'item2',
      Reason6Enum::OTHER_PARTY
    ),
    GuideDropped.new(
      'item2',
      Reason6Enum::OTHER_PARTY
    )
  ],
  FallbackReasonEnum::PROVIDER_ERROR,
  false,
  TemplateEnum::SUBTRACTION
)
```



