# Time Evidence 1

Source: http://localhost:3000/#/ruby/x-redirect/JTI0bSUyRlRpbWVFdmlkZW5jZTE

Time evidence.


# Class Name

`TimeEvidence1`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `advisory_only` | `TrueClass \| FalseClass` | Optional | Advisory only. |
| `events` | Array[[MessageTimeEvent](http://localhost:3000/llms-pages/ruby/models/structures/message-time-event.md) \| [TimeEvent](http://localhost:3000/llms-pages/ruby/models/structures/time-event.md)] \| nil | Optional | This is Array of a container for any-of cases.<br><br>**Constraints**: *Minimum Items*: `2`, *Maximum Items*: `30` |
| `flags` | [`Array[FlagEnum]`](http://localhost:3000/llms-pages/ruby/models/enumerations/flag.md) | Optional | Flags.<br><br>**Constraints**: *Maximum Items*: `4` |
| `gaps_seconds` | [`TimeGaps`](http://localhost:3000/llms-pages/ruby/models/structures/time-gaps.md) | Optional | TimeGaps. |
| `judgement` | [`JudgementEnum`](http://localhost:3000/llms-pages/ruby/models/enumerations/judgement.md) | Optional | Judgement. |
| `schema_version` | [`SchemaVersionEnum`](http://localhost:3000/llms-pages/ruby/models/enumerations/schema-version.md) | Optional | Schema version. |


# Example

```ruby
time_evidence1 = TimeEvidence1.new(
  false,
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
    )
  ],
  [
    FlagEnum::DELIVERY_AFTER_CLAIM,
    FlagEnum::CLAIM_TIME_EARLIER_THAN_PAYMENT_TIME
  ],
  TimeGaps.new(
    210,
    154,
    192,
    208
  ),
  JudgementEnum::NOT_MADE,
  envrr
)
```



