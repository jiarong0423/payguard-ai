# Guide State Response Reply

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRkd1aWRlU3RhdGVSZXNwb25zZVJlcGx5


# Data Type

`GuideReply`


# Cases

| Type |
|  --- |
| [`GuideReply`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/guide-reply.md) |


# GuideReply

## Initialization Code

### Example

```php
$value = GuideReplyBuilder::init(
    ChooserEnum::FORM,
    [
        GuideDroppedBuilder::init(
            'item2',
            Reason6Enum::OTHER_PARTY
        )->build()
    ],
    FallbackReasonEnum::LATE,
    false,
    TemplateEnum::REVIEW,
    'text0'
)->build();
```



