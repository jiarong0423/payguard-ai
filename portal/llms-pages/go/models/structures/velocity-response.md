# Velocity Response

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRlZlbG9jaXR5UmVzcG9uc2U

VelocityResponse.


# Class Name

`VelocityResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AdvisoryOnly` | `string` | Required, Constant | Advisory only.<br><br>**Value**: `"True"` |
| `Alert` | `bool` | Required | Alert. |
| `BaselineAmountPerHour` | `string` | Required | Baseline amount per hour. |
| `BaselineProvenance` | [`models.BaselineProvenanceEnum`](http://localhost:3000/llms-pages/go/models/enumerations/baseline-provenance.md) | Required | Baseline provenance. |
| `BaselineWindowEnd` | `string` | Required | Baseline window end. |
| `BaselineWindowStart` | `string` | Required | Baseline window start. |
| `Currency` | [`models.VelocityResponseCurrency`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/velocity-response-currency.md) | Required | This is a container for any-of cases. |
| `CurrentAmountPerHour` | `string` | Required | Current amount per hour. |
| `ExcludedFutureCount` | `int` | Required | Excluded future count. |
| `ExcludedPastCount` | `int` | Required | Excluded past count. |
| `Limitations` | `[]string` | Required | Limitations. |
| `PolicyVersion` | `string` | Required | Policy version. |
| `Ratio` | [`models.VelocityResponseRatio`](http://localhost:3000/llms-pages/go/models/oneof-anyof-definitions/velocity-response-ratio.md) | Required | This is a container for any-of cases. |
| `Status` | [`models.Status14Enum`](http://localhost:3000/llms-pages/go/models/enumerations/status-14.md) | Required | Status. |
| `Threshold` | `string` | Required | Threshold. |
| `TotalAmount` | `string` | Required | Total amount. |
| `TransactionCount` | `int` | Required | Transaction count. |
| `WindowBoundary` | `string` | Required, Constant | Window boundary.<br><br>**Value**: `"left_open_right_closed"` |
| `WindowEnd` | `string` | Required | Window end. |
| `WindowHours` | `int` | Required | Window hours. |
| `WindowStart` | `string` | Required | Window start. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    velocityResponse := models.VelocityResponse{
        AdvisoryOnly:          "True",
        Alert:                 false,
        BaselineAmountPerHour: "baseline_amount_per_hour4",
        BaselineProvenance:    models.BaselineProvenanceEnum_SYNTHETICBASELINE,
        BaselineWindowEnd:     "baseline_window_end6",
        BaselineWindowStart:   "baseline_window_start0",
        Currency:              models.VelocityResponseCurrencyContainer.FromString("String1"),
        CurrentAmountPerHour:  "current_amount_per_hour4",
        ExcludedFutureCount:   6,
        ExcludedPastCount:     154,
        Limitations:           []string{
            "limitations9",
            "limitations8",
            "limitations7",
        },
        PolicyVersion:         "policy_version8",
        Ratio:                 models.VelocityResponseRatioContainer.FromString("String1"),
        Status:                models.Status14Enum_NORMAL,
        Threshold:             "threshold8",
        TotalAmount:           "total_amount6",
        TransactionCount:      134,
        WindowBoundary:        "left_open_right_closed",
        WindowEnd:             "window_end0",
        WindowHours:           20,
        WindowStart:           "window_start6",
    }

}
```



