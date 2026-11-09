# Guide State Response Analysis

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0bSUyRkd1aWRlU3RhdGVSZXNwb25zZUFuYWx5c2lz


# Class Name

`GuideStateResponseAnalysis`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`GuideAnalysis`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/guide-analysis.md) | GuideStateResponseAnalysis.fromGuideAnalysis(GuideAnalysis guideAnalysis) |


# GuideAnalysis

## Initialization Code

### Example

```java
GuideStateResponseAnalysis.fromGuideAnalysis(
        new GuideAnalysis.Builder(
            GuideAnalysisReason.fromReason5(
                Reason5Enum.INVALID_REPLY
            ),
            Status8Enum.REPLACED,
            186
        )
        .build()
    )
```



