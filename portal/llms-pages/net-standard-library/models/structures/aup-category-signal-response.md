# Aup Category Signal Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkF1cENhdGVnb3J5U2lnbmFsUmVzcG9uc2U

Optional Channel3 signal shown next to the AUP result; it never changes the rule decision.


# Class Name

`AupCategorySignalResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `AffectsDecision` | `string` | Required, Constant | Affects decision.<br><br>**Value**: `"False"` |
| `Reason` | [`AupCategorySignalResponseReason`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/aup-category-signal-response-reason.md) | Required | This is a container for any-of cases. |
| `Signal` | [`AupCategorySignalResponseSignal`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/aup-category-signal-response-signal.md) | Required | This is a container for any-of cases. |
| `Status` | [`Status2Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/status-2.md) | Required | Status. |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;
using TradeGlotLocalConsole.Standard.Models.Containers;

AupCategorySignalResponse aupCategorySignalResponse = new AupCategorySignalResponse
{
    AffectsDecision = "False",
    Reason = AupCategorySignalResponseReason.FromReason(ReasonEnum.BudgetExhausted),
    Signal = AupCategorySignalResponseSignal.FromCategorySignal(
        new CategorySignal
        {
            Category = CategorySignalCategory.FromString("String9"),
            Confidence = CategorySignalConfidence.FromConfidence(ConfidenceEnum.HIGH),
            Source = "channel3",
        }
    ),
    Status = Status2Enum.NOTSENT,
};
```



