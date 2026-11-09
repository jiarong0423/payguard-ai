# Reply

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRlJlcGx5

Reply.


# Class Name

`Reply`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `chooser` | [`ChooserEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/chooser.md) | Optional | Chooser. |
| `dropped` | [`Array[GuideDropped]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/guide-dropped.md) | Optional | Dropped. |
| `fallback_reason` | [FallbackReason](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/fallback-reason.md) \| nil | Optional | This is a container for any-of cases. |
| `state_changed` | `TrueClass \| FalseClass` | Optional | State changed. |
| `template` | [`TemplateEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/template.md) | Optional | Template. |
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



