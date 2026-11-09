# Dispute Summary

Source: http://localhost:3000/#/go/x-redirect/JTI0bSUyRkRpc3B1dGVTdW1tYXJ5

DisputeSummary.


# Class Name

`DisputeSummary`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `CaseRef` | `string` | Required | Case ref. |
| `DisputeAmount` | [`models.SyntheticMoney`](http://localhost:3000/llms-pages/go/models/structures/synthetic-money.md) | Required | Same shape as the PayPal Disputes `dispute_amount` (ProviderMoney below); values are synthetic. |
| `OpenedAt` | `string` | Required | Opened at. |
| `OrderRef` | `string` | Required | Order ref. |
| `Reason` | `string` | Required | Reason. |
| `SellerResponseDueDate` | `string` | Required | Seller response due date. |
| `Status` | [`models.Status7Enum`](http://localhost:3000/llms-pages/go/models/enumerations/status-7.md) | Required | Status. |


# Example

```go
package main

import (
    "tradeglotlocalconsole/models"
)

func main() {
    disputeSummary := models.DisputeSummary{
        CaseRef:               "case_ref6",
        DisputeAmount:         models.SyntheticMoney{
            CurrencyCode: "currency_code6",
            Value:        "value0",
        },
        OpenedAt:              "opened_at0",
        OrderRef:              "order_ref8",
        Reason:                "reason8",
        SellerResponseDueDate: "seller_response_due_date0",
        Status:                models.Status7Enum_NEEDSREVIEW,
    }

}
```



