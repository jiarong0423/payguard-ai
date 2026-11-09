# Time Evidence

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRlRpbWVFdmlkZW5jZQ

TimeEvidence.


# Class Name

`TimeEvidence`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `advisory_only` | `String` | Required, Constant | Advisory only.<br><br>**Value**: `'True'` |
| `events` | Array[[MessageTimeEvent](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/message-time-event.md) \| [TimeEvent](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/time-event.md)] | Required | This is Array of a container for any-of cases.<br><br>**Constraints**: *Minimum Items*: `2`, *Maximum Items*: `30` |
| `flags` | [`Array[FlagEnum]`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/flag.md) | Required | Flags.<br><br>**Constraints**: *Maximum Items*: `4` |
| `gaps_seconds` | [`TimeGaps`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/time-gaps.md) | Required | TimeGaps. |
| `judgement` | `String` | Required, Constant | Judgement.<br><br>**Value**: `'NOT_MADE'` |
| `schema_version` | `String` | Required, Constant | Schema version.<br><br>**Value**: `'payguard.time_evidence.v1'` |


# Example

```ruby
time_evidence = TimeEvidence.new(
  'True',
  [
    MessageTimeEvent.new(
      'at4',
      ChannelEnum::EMAIL,
      DirectionEnum::INBOUND,
      'kind6',
      'message_digest2',
      'source4',
      TopicEnum::ORDER_DETAILS_PROVIDED
    ),
    MessageTimeEvent.new(
      'at4',
      ChannelEnum::EMAIL,
      DirectionEnum::INBOUND,
      'kind6',
      'message_digest2',
      'source4',
      TopicEnum::ORDER_DETAILS_PROVIDED
    ),
    MessageTimeEvent.new(
      'at4',
      ChannelEnum::EMAIL,
      DirectionEnum::INBOUND,
      'kind6',
      'message_digest2',
      'source4',
      TopicEnum::ORDER_DETAILS_PROVIDED
    )
  ],
  [
    FlagEnum::ORDER_RECORD_ABSENT
  ],
  TimeGaps.new(
    210,
    154,
    192,
    208
  ),
  'NOT_MADE',
  'payguard.time_evidence.v1'
)
```



