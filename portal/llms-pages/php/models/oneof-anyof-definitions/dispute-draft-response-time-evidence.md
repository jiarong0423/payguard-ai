# Dispute Draft Response Time Evidence

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRkRpc3B1dGVEcmFmdFJlc3BvbnNlVGltZUV2aWRlbmNl


# Data Type

`TimeEvidence`


# Cases

| Type |
|  --- |
| [`TimeEvidence`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/time-evidence.md) |


# TimeEvidence

## Initialization Code

### Example

```php
$value = TimeEvidenceBuilder::init(
    [
        MessageTimeEventBuilder::init(
            'at4',
            ChannelEnum::EMAIL,
            DirectionEnum::INBOUND,
            'message_digest2',
            TopicEnum::ORDER_DETAILS_PROVIDED
        )->build()
    ],
    [
        FlagEnum::ORDER_RECORD_ABSENT,
        FlagEnum::DELIVERY_NOT_RECORDED,
        FlagEnum::DELIVERY_AFTER_CLAIM
    ],
    TimeGapsBuilder::init(
        210,
        154,
        192,
        208
    )->build()
)->build();
```



