# Guide State Response Reply

Source: http://localhost:3000/#/php/x-redirect/JTI0bSUyRkd1aWRlU3RhdGVSZXNwb25zZVJlcGx5


# Data Type

`GuideReply`


# Cases

| Type |
|  --- |
| [`GuideReply`](http://localhost:3000/llms-pages/php/models/structures/guide-reply.md) |


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



