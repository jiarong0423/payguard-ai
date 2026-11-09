# Dispute Summary

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0bSUyRkRpc3B1dGVTdW1tYXJ5

DisputeSummary.


# Class Name

`DisputeSummary`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `CaseRef` | `string` | Required | Case ref. |
| `DisputeAmount` | [`SyntheticMoney`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/synthetic-money.md) | Required | Same shape as the PayPal Disputes `dispute_amount` (ProviderMoney below); values are synthetic. |
| `OpenedAt` | `string` | Required | Opened at. |
| `OrderRef` | `string` | Required | Order ref. |
| `Reason` | `string` | Required | Reason. |
| `SellerResponseDueDate` | `string` | Required | Seller response due date. |
| `Status` | [`Status7Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/enumerations/status-7.md) | Required | Status. |


# Example

```csharp
using TradeGlotLocalConsole.Standard.Models;

DisputeSummary disputeSummary = new DisputeSummary
{
    CaseRef = "case_ref6",
    DisputeAmount = new SyntheticMoney
    {
        CurrencyCode = "currency_code6",
        MValue = "value0",
    },
    OpenedAt = "opened_at0",
    OrderRef = "order_ref8",
    Reason = "reason8",
    SellerResponseDueDate = "seller_response_due_date0",
    Status = Status7Enum.NeedsReview,
};
```



