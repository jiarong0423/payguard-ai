# Analysis

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRkFuYWx5c2lz

Analysis.


# Class Name

`Analysis`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `Reason` | [`AnalysisReason`](http://localhost:3000/llms-pages/java/models/oneof-anyof-definitions/analysis-reason.md) | Optional | This is a container for any-of cases. | AnalysisReason getReason() | setReason(AnalysisReason reason) |
| `Status` | [`Status8Enum`](http://localhost:3000/llms-pages/java/models/enumerations/status-8.md) | Optional | Status. | Status8Enum getStatus() | setStatus(Status8Enum status) |
| `Turn` | `Integer` | Optional | Turn. | Integer getTurn() | setTurn(Integer turn) |


# Example

```java
import m18000.m0.m0.m127.models.Analysis;
import m18000.m0.m0.m127.models.Reason5Enum;
import m18000.m0.m0.m127.models.Status8Enum;
import m18000.m0.m0.m127.models.containers.AnalysisReason;

Analysis analysis = new Analysis.Builder()
    .reason(AnalysisReason.fromReason5(
        Reason5Enum.INVALID_REPLY
    ))
    .status(Status8Enum.REPLACED)
    .turn(198)
    .build();
```



