# Dispute Draft Response Time Evidence

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkRpc3B1dGVEcmFmdFJlc3BvbnNlVGltZUV2aWRlbmNl


# Data Type

`TimeEvidence`


# Cases

| Type |
|  --- |
| [`TimeEvidence`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/time-evidence.md) |


# TimeEvidence

## Initialization Code

### Example

```ruby
value = TimeEvidence.new(
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
    )
  ],
  [
    FlagEnum::ORDER_RECORD_ABSENT,
    FlagEnum::DELIVERY_NOT_RECORDED,
    FlagEnum::DELIVERY_AFTER_CLAIM
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



