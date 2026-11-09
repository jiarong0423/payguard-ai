# Guide Reply Fallback Reason

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkd1aWRlUmVwbHlGYWxsYmFja1JlYXNvbg


# Class Name

`GuideReplyFallbackReason`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`models.FallbackReasonEnum`](http://localhost:3000/llms-pages/go/models/enumerations/fallback-reason.md) | models.GuideReplyFallbackReasonContainer.FromFallbackReason(models.FallbackReasonEnum fallbackReason) |


# models.FallbackReasonEnum

## Initialization Code

### Example

```go
value := models.GuideReplyFallbackReasonContainer.FromFallbackReason(models.FallbackReasonEnum_BUDGET)
```



