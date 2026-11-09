# Guide Reply

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkd1aWRlUmVwbHk

GuideReply.


# Class Name

`GuideReply`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `chooser` | [`ChooserEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/chooser.md) | Required | Chooser. |
| `dropped` | [`Array[GuideDropped]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/guide-dropped.md) | Required | Dropped. |
| `fallback_reason` | [FallbackReason](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/fallback-reason.md) | Required | This is a container for any-of cases. |
| `state_changed` | `TrueClass \| FalseClass` | Required | State changed. |
| `template` | [`TemplateEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/template.md) | Required | Template. |
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



