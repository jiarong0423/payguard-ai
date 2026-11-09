# Guide Analysis

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRkd1aWRlQW5hbHlzaXM

GuideAnalysis.


# Class Name

`GuideAnalysis`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Reason` | [`GuideAnalysisReason`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/guide-analysis-reason.md) | Required | This is a container for any-of cases. | GuideAnalysisReason getReason() | setReason(GuideAnalysisReason reason) |
| `Status` | [`Status8Enum`](http://localhost:3000/llms-pages/java/models/enumerations/status-8.md) | Required | Status. | Status8Enum getStatus() | setStatus(Status8Enum status) |
| `Turn` | `int` | Required | Turn. | int getTurn() | setTurn(int turn) |


# Example

```java
import m18000.m0.m0.m127.models.GuideAnalysis;
import m18000.m0.m0.m127.models.Reason5Enum;
import m18000.m0.m0.m127.models.Status8Enum;
import m18000.m0.m0.m127.models.containers.GuideAnalysisReason;

GuideAnalysis guideAnalysis = new GuideAnalysis.Builder(
    GuideAnalysisReason.fromReason5(
        Reason5Enum.INVALID_REPLY
    ),
    Status8Enum.ANALYSING,
    236
)
.build();
```



