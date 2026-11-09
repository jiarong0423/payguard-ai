# Aup Category Signal Response

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkF1cENhdGVnb3J5U2lnbmFsUmVzcG9uc2U

Optional Channel3 signal shown next to the AUP result; it never changes the rule decision.


# Class Name

`AupCategorySignalResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AffectsDecision` | `string` | Required, Constant | Affects decision.<br><br>**Value**: `"False"` |
| `Reason` | [`models.AupCategorySignalResponseReason`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/aup-category-signal-response-reason.md) | Required | This is a container for any-of cases. |
| `Signal` | [`models.AupCategorySignalResponseSignal`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/aup-category-signal-response-signal.md) | Required | This is a container for any-of cases. |
| `Status` | [`models.Status2Enum`](http://localhost:3000/llms-pages/go/models/enumerations/status-2.md) | Required | Status. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    aupCategorySignalResponse := models.AupCategorySignalResponse{
        AffectsDecision: "False",
        Reason:          models.AupCategorySignalResponseReasonContainer.FromReason(models.ReasonEnum_BUDGETEXHAUSTED),
        Signal:          models.AupCategorySignalResponseSignalContainer.FromCategorySignal(models.CategorySignal{
            Category:             models.CategorySignalCategoryContainer.FromString("String9"),
            Confidence:           models.CategorySignalConfidenceContainer.FromConfidence(models.ConfidenceEnum_HIGH),
            Source:               "channel3",
        }),
        Status:          models.Status2Enum_NOTSENT,
    }

}
```



