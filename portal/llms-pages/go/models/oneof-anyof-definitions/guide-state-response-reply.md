# Guide State Response Reply

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkd1aWRlU3RhdGVSZXNwb25zZVJlcGx5


# Class Name

`GuideStateResponseReply`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`models.GuideReply`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/guide-reply.md) | models.GuideStateResponseReplyContainer.FromGuideReply(models.GuideReply guideReply) |


# models.GuideReply

## Initialization Code

### Example

```go
value := models.GuideStateResponseReplyContainer.FromGuideReply(models.GuideReply{
    Chooser:        models.ChooserEnum_FORM,
    Dropped:        []models.GuideDropped{
        models.GuideDropped{
            Item:   "item2",
            Reason: models.Reason6Enum_OTHERPARTY,
        },
    },
    FallbackReason: models.GuideReplyFallbackReasonContainer.FromFallbackReason(models.FallbackReasonEnum_LATE),
    StateChanged:   false,
    Template:       models.TemplateEnum_REVIEW,
    Text:           "text0",
})
```



