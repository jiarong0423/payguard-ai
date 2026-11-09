# Guide State Response Analysis

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRkd1aWRlU3RhdGVSZXNwb25zZUFuYWx5c2lz


# Class Name

`GuideStateResponseAnalysis`


# Cases

| Type | Factory Method |
|  --- | --- |
| [`GuideAnalysis`](http://localhost:3000/llms-pages/java/models/structures/guide-analysis.md) | GuideStateResponseAnalysis.fromGuideAnalysis(GuideAnalysis guideAnalysis) |


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



