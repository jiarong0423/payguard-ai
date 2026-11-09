# State Response

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRlN0YXRlUmVzcG9uc2U

StateResponse.


# Class Name

`StateResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Activity` | [`[]models.Activity`](http://localhost:3000/llms-pages/go/models/structures/activity.md) | Required | Activity. |
| `Disputes` | [`[]models.DisputeSummary`](http://localhost:3000/llms-pages/go/models/structures/dispute-summary.md) | Required | Disputes. |
| `ExpiresAt` | `string` | Required | Expires at. |
| `PolicyVersion` | `string` | Required | Policy version. |
| `Scenario` | [`models.Scenario`](http://localhost:3000/llms-pages/go/models/structures/scenario.md) | Required | Scenario. |
| `SessionId` | `string` | Required | Session id. |
| `Source` | `string` | Required, Constant | Source.<br><br>**Value**: `"synthetic"` |
| `Transactions` | [`[]models.Transaction`](http://localhost:3000/llms-pages/go/models/structures/transaction.md) | Required | Transactions. |
| `Velocity` | [`models.VelocityResponse`](http://localhost:3000/llms-pages/go/models/structures/velocity-response.md) | Required | VelocityResponse. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    stateResponse := models.StateResponse{
        Activity:      []models.Activity{
            models.Activity{
                At:     "at4",
                Id:     "id8",
                Kind:   "kind6",
                Label:  "label8",
                Source: "synthetic",
            },
        },
        Disputes:      []models.DisputeSummary{
            models.DisputeSummary{
                CaseRef:               "case_ref6",
                DisputeAmount:         models.SyntheticMoney{
                    CurrencyCode: "currency_code6",
                    Value:        "value0",
                },
                OpenedAt:              "opened_at0",
                OrderRef:              "order_ref8",
                Reason:                "reason2",
                SellerResponseDueDate: "seller_response_due_date0",
                Status:                models.Status7Enum_NEEDSREVIEW,
            },
        },
        ExpiresAt:     "expires_at6",
        PolicyVersion: "policy_version8",
        Scenario:      models.Scenario{
            Burst:   false,
            Dispute: false,
        },
        SessionId:     "session_id2",
        Source:        "synthetic",
        Transactions:  []models.Transaction{
            models.Transaction{
                Amount:     "amount0",
                Currency:   "currency8",
                OccurredAt: "occurred_at2",
                OrderId:    "order_id2",
            },
        },
        Velocity:      models.VelocityResponse{
            AdvisoryOnly:          "True",
            Alert:                 false,
            BaselineAmountPerHour: "baseline_amount_per_hour0",
            BaselineProvenance:    models.BaselineProvenanceEnum_SYNTHETICBASELINE,
            BaselineWindowEnd:     "baseline_window_end2",
            BaselineWindowStart:   "baseline_window_start4",
            Currency:              models.VelocityResponseCurrencyContainer.FromString("String7"),
            CurrentAmountPerHour:  "current_amount_per_hour0",
            ExcludedFutureCount:   240,
            ExcludedPastCount:     132,
            Limitations:           []string{
                "limitations7",
            },
            PolicyVersion:         "policy_version4",
            Ratio:                 models.VelocityResponseRatioContainer.FromString("String5"),
            Status:                models.Status14Enum_INSUFFICIENTBASELINE,
            Threshold:             "threshold4",
            TotalAmount:           "total_amount2",
            TransactionCount:      112,
            WindowBoundary:        "left_open_right_closed",
            WindowEnd:             "window_end6",
            WindowHours:           2,
            WindowStart:           "window_start8",
        },
    }

}
```



