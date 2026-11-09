# Guide State Response Reply

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkd1aWRlU3RhdGVSZXNwb25zZVJlcGx5


# Class Name

`GuideStateResponseReply`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`GuideReply`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/guide-reply.md) | GuideStateResponseReply.fromGuideReply(GuideReply guideReply) |


# GuideReply

## Initialization Code

### Example

```java
GuideStateResponseReply.fromGuideReply(
        new GuideReply.Builder(
            ChooserEnum.FORM,
            Arrays.asList(
                new GuideDropped.Builder(
                    "item2",
                    Reason6Enum.OTHER_PARTY
                )
                .build()
            ),
            GuideReplyFallbackReason.fromFallbackReason(
                FallbackReasonEnum.LATE
            ),
            false,
            TemplateEnum.REVIEW,
            "text0"
        )
        .build()
    )
```



