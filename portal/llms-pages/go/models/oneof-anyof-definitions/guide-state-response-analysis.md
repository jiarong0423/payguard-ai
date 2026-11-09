# Guide State Response Analysis

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0bSUyRkd1aWRlU3RhdGVSZXNwb25zZUFuYWx5c2lz


# Class Name

`GuideStateResponseAnalysis`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`models.GuideAnalysis`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/guide-analysis.md) | models.GuideStateResponseAnalysisContainer.FromGuideAnalysis(models.GuideAnalysis guideAnalysis) |


# models.GuideAnalysis

## Initialization Code

### Example

```go
value := models.GuideStateResponseAnalysisContainer.FromGuideAnalysis(models.GuideAnalysis{
    Reason: models.GuideAnalysisReasonContainer.FromReason5(models.Reason5Enum_INVALIDREPLY),
    Status: models.Status8Enum_REPLACED,
    Turn:   186,
})
```



