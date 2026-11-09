# Guide Reply

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRkd1aWRlUmVwbHk

GuideReply.


# Class Name

`GuideReply`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `chooser` | [`ChooserEnum`](http://localhost:3000/llms-pages/ruby/models/enumerations/chooser.md) | Required | Chooser. |
| `dropped` | [`Array[GuideDropped]`](http://localhost:3000/llms-pages/ruby/models/structures/guide-dropped.md) | Required | Dropped. |
| `fallback_reason` | [FallbackReason](http://localhost:3000/llms-pages/ruby/models/enumerations/fallback-reason.md) | Required | This is a container for any-of cases. |
| `state_changed` | `TrueClass \| FalseClass` | Required | State changed. |
| `template` | [`TemplateEnum`](http://localhost:3000/llms-pages/ruby/models/enumerations/template.md) | Required | Template. |
| `text` | `String` | Required | Text.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `400` |


# Example

```ruby
guide_reply = GuideReply.new(
  ChooserEnum::MODEL,
  [
    GuideDropped.new(
      'item2',
      Reason6Enum::OTHER_PARTY
    )
  ],
  FallbackReasonEnum::BUDGET,
  false,
  TemplateEnum::OTHER_PARTY,
  'text2'
)
```



