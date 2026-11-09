# Dispute Summary

Source: http://localhost:3000/#/java/x-redirect/JTI0bSUyRkRpc3B1dGVTdW1tYXJ5

DisputeSummary.


# Class Name

`DisputeSummary`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `CaseRef` | `String` | Required | Case ref. | String getCaseRef() | setCaseRef(String caseRef) |
| `DisputeAmount` | [`SyntheticMoney`](http://localhost:3000/llms-pages/java/models/structures/synthetic-money.md) | Required | Same shape as the PayPal Disputes `dispute_amount` (ProviderMoney below); values are synthetic. | SyntheticMoney getDisputeAmount() | setDisputeAmount(SyntheticMoney disputeAmount) |
| `OpenedAt` | `String` | Required | Opened at. | String getOpenedAt() | setOpenedAt(String openedAt) |
| `OrderRef` | `String` | Required | Order ref. | String getOrderRef() | setOrderRef(String orderRef) |
| `Reason` | `String` | Required | Reason. | String getReason() | setReason(String reason) |
| `SellerResponseDueDate` | `String` | Required | Seller response due date. | String getSellerResponseDueDate() | setSellerResponseDueDate(String sellerResponseDueDate) |
| `Status` | [`Status7Enum`](http://localhost:3000/llms-pages/java/models/enumerations/status-7.md) | Required | Status. | Status7Enum getStatus() | setStatus(Status7Enum status) |


# Example

```java
import m18000.m0.m0.m127.models.DisputeSummary;
import m18000.m0.m0.m127.models.Status7Enum;
import m18000.m0.m0.m127.models.SyntheticMoney;

DisputeSummary disputeSummary = new DisputeSummary.Builder(
    "case_ref6",
    new SyntheticMoney.Builder(
        "currency_code6",
        "value0"
    )
    .build(),
    "opened_at0",
    "order_ref8",
    "reason8",
    "seller_response_due_date0",
    Status7Enum.NEEDS_REVIEW
)
.build();
```



