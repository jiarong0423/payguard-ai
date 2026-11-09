# Guide Reply Fallback Reason

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkd1aWRlUmVwbHlGYWxsYmFja1JlYXNvbg


# Class Name

`GuideReplyFallbackReason`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`models.FallbackReasonEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/enumerations/fallback-reason.md) | models.GuideReplyFallbackReasonContainer.FromFallbackReason(models.FallbackReasonEnum fallbackReason) |


# models.FallbackReasonEnum

## Initialization Code

### Example

```go
value := models.GuideReplyFallbackReasonContainer.FromFallbackReason(models.FallbackReasonEnum_BUDGET)
```



