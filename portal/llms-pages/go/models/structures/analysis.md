# Analysis

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkFuYWx5c2lz

Analysis.


# Class Name

`Analysis`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Reason` | [`*models.AnalysisReason`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/analysis-reason.md) | Optional | This is a container for any-of cases. |
| `Status` | [`*models.Status8Enum`](http://localhost:3000/llms-pages/go/models/enumerations/status-8.md) | Optional | Status. |
| `Turn` | `*int` | Optional | Turn. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    analysis := models.Analysis{
        Reason:               models.ToPointer(models.AnalysisReasonContainer.FromReason5(models.Reason5Enum_INVALIDREPLY)),
        Status:               models.ToPointer(models.Status8Enum_REPLACED),
        Turn:                 models.ToPointer(198),
    }

}
```



