# State Response

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0bSUyRlN0YXRlUmVzcG9uc2U

StateResponse.


# Class Name

`StateResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `Activity` | [`List<Activity>`](http://localhost:3000/llms-pages/net-standard-library/models/structures/activity.md) | Required | Activity. |
| `Disputes` | [`List<DisputeSummary>`](http://localhost:3000/llms-pages/net-standard-library/models/structures/dispute-summary.md) | Required | Disputes. |
| `ExpiresAt` | `string` | Required | Expires at. |
| `PolicyVersion` | `string` | Required | Policy version. |
| `Scenario` | [`Scenario`](http://localhost:3000/llms-pages/net-standard-library/models/structures/scenario.md) | Required | Scenario. |
| `SessionId` | `string` | Required | Session id. |
| `Source` | `string` | Required, Constant | Source.<br><br>**Value**: `"synthetic"` |
| `Transactions` | [`List<Transaction>`](http://localhost:3000/llms-pages/net-standard-library/models/structures/transaction.md) | Required | Transactions. |
| `Velocity` | [`VelocityResponse`](http://localhost:3000/llms-pages/net-standard-library/models/structures/velocity-response.md) | Required | VelocityResponse. |


# Example

```csharp
using System.Collections.Generic;
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

StateResponse stateResponse = new StateResponse
{
    Activity = new List<Activity>
    {
        new Activity
        {
            At = "at4",
            Id = "id8",
            Kind = "kind6",
            Label = "label8",
            Source = "synthetic",
        },
    },
    Disputes = new List<DisputeSummary>
    {
        new DisputeSummary
        {
            CaseRef = "case_ref6",
            DisputeAmount = new SyntheticMoney
            {
                CurrencyCode = "currency_code6",
                MValue = "value0",
            },
            OpenedAt = "opened_at0",
            OrderRef = "order_ref8",
            Reason = "reason2",
            SellerResponseDueDate = "seller_response_due_date0",
            Status = Status7Enum.NeedsReview,
        },
    },
    ExpiresAt = "expires_at6",
    PolicyVersion = "policy_version8",
    Scenario = new Scenario
    {
        Burst = false,
        Dispute = false,
    },
    SessionId = "session_id2",
    Source = "synthetic",
    Transactions = new List<Transaction>
    {
        new Transaction
        {
            Amount = "amount0",
            Currency = "currency8",
            OccurredAt = "occurred_at2",
            OrderId = "order_id2",
        },
    },
    Velocity = new VelocityResponse
    {
        AdvisoryOnly = "True",
        Alert = false,
        BaselineAmountPerHour = "baseline_amount_per_hour0",
        BaselineProvenance = BaselineProvenanceEnum.SYNTHETICBASELINE,
        BaselineWindowEnd = "baseline_window_end2",
        BaselineWindowStart = "baseline_window_start4",
        Currency = VelocityResponseCurrency.FromString("String7"),
        CurrentAmountPerHour = "current_amount_per_hour0",
        ExcludedFutureCount = 240,
        ExcludedPastCount = 132,
        Limitations = new List<string>
        {
            "limitations7",
        },
        PolicyVersion = "policy_version4",
        Ratio = VelocityResponseRatio.FromString("String5"),
        Status = Status14Enum.InsufficientBaseline,
        Threshold = "threshold4",
        TotalAmount = "total_amount2",
        TransactionCount = 112,
        WindowBoundary = "left_open_right_closed",
        WindowEnd = "window_end6",
        WindowHours = 2,
        WindowStart = "window_start8",
    },
};
```



