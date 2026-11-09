# Guide State Response Reply

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkd1aWRlU3RhdGVSZXNwb25zZVJlcGx5


# Data Type

`GuideReply`


# Cases

| Type |
|  --- |
| [`GuideReply`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/guide-reply.md) |


# GuideReply

## Initialization Code

### Example

```python
value = GuideReply(
    chooser=ChooserEnum.FORM,
    dropped=[
        GuideDropped(
            item='item2',
            reason=Reason6Enum.OTHER_PARTY
        )
    ],
    fallback_reason=FallbackReasonEnum.LATE,
    state_changed=False,
    template=TemplateEnum.REVIEW,
    text='text0'
)
```



