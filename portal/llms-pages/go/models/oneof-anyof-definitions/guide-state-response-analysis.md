# Guide State Response Analysis

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkd1aWRlU3RhdGVSZXNwb25zZUFuYWx5c2lz


# Class Name

`GuideStateResponseAnalysis`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`models.GuideAnalysis`](http://localhost:3000/llms-pages/go/models/structures/guide-analysis.md) | models.GuideStateResponseAnalysisContainer.FromGuideAnalysis(models.GuideAnalysis guideAnalysis) |


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



