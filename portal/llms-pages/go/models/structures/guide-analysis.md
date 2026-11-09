# Guide Analysis

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkd1aWRlQW5hbHlzaXM

GuideAnalysis.


# Class Name

`GuideAnalysis`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Reason` | [`models.GuideAnalysisReason`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/guide-analysis-reason.md) | Required | This is a container for any-of cases. |
| `Status` | [`models.Status8Enum`](http://localhost:3000/llms-pages/go/models/enumerations/status-8.md) | Required | Status. |
| `Turn` | `int` | Required | Turn. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    guideAnalysis := models.GuideAnalysis{
        Reason: models.GuideAnalysisReasonContainer.FromReason5(models.Reason5Enum_INVALIDREPLY),
        Status: models.Status8Enum_ANALYSING,
        Turn:   236,
    }

}
```



