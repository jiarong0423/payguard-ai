# Guide State Response Analysis

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkd1aWRlU3RhdGVSZXNwb25zZUFuYWx5c2lz


# Class Name

`GuideStateResponseAnalysis`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`GuideAnalysis`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/guide-analysis.md) | GuideStateResponseAnalysis.FromGuideAnalysis(GuideAnalysis guideAnalysis) |


# GuideAnalysis

## Initialization Code

### Example

```csharp
GuideStateResponseAnalysis value = GuideStateResponseAnalysis.FromGuideAnalysis(
    new GuideAnalysis
    {
        Reason = GuideAnalysisReason.FromReason5(Reason5Enum.InvalidReply),
        Status = Status8Enum.Replaced,
        Turn = 186,
    }
);
```



