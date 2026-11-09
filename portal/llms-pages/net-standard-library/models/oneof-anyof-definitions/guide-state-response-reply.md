# Guide State Response Reply

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRkd1aWRlU3RhdGVSZXNwb25zZVJlcGx5


# Class Name

`GuideStateResponseReply`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`GuideReply`](http://localhost:3000/llms-pages/net-standard-library/models/structures/guide-reply.md) | GuideStateResponseReply.FromGuideReply(GuideReply guideReply) |


# GuideReply

## Initialization Code

### Example

```csharp
GuideStateResponseReply value = GuideStateResponseReply.FromGuideReply(
    new GuideReply
    {
        Chooser = ChooserEnum.Form,
        Dropped = new List<GuideDropped>
        {
            new GuideDropped
            {
                Item = "item2",
                Reason = Reason6Enum.OtherParty,
            },
        },
        FallbackReason = GuideReplyFallbackReason.FromFallbackReason(FallbackReasonEnum.Late),
        StateChanged = false,
        Template = TemplateEnum.REVIEW,
        Text = "text0",
    }
);
```



