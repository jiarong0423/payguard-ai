# Dispute Summary

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0bSUyRkRpc3B1dGVTdW1tYXJ5

DisputeSummary.


# Class Name

`DisputeSummary`


# Fields

| Name | Type | Tags | Description | Getter | Setter |
|  --- | --- | --- | --- | --- | --- |
| `caseRef` | `string` | Required | Case ref. | getCaseRef(): string | setCaseRef(string caseRef): void |
| `disputeAmount` | [`SyntheticMoney`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/synthetic-money.md) | Required | Same shape as the PayPal Disputes `dispute_amount` (ProviderMoney below); values are synthetic. | getDisputeAmount(): SyntheticMoney | setDisputeAmount(SyntheticMoney disputeAmount): void |
| `openedAt` | `string` | Required | Opened at. | getOpenedAt(): string | setOpenedAt(string openedAt): void |
| `orderRef` | `string` | Required | Order ref. | getOrderRef(): string | setOrderRef(string orderRef): void |
| `reason` | `string` | Required | Reason. | getReason(): string | setReason(string reason): void |
| `sellerResponseDueDate` | `string` | Required | Seller response due date. | getSellerResponseDueDate(): string | setSellerResponseDueDate(string sellerResponseDueDate): void |
| `status` | [`string(Status7Enum)`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/enumerations/status-7.md) | Required | Status. | getStatus(): string | setStatus(string status): void |


# Example

```php
use TradeGlotLocalConsoleLib\Models\Builders\DisputeSummaryBuilder;
use TradeGlotLocalConsoleLib\Models\Builders\SyntheticMoneyBuilder;
use TradeGlotLocalConsoleLib\Models\Status7Enum;

$disputeSummary = DisputeSummaryBuilder::init(
    'case_ref6',
    SyntheticMoneyBuilder::init(
        'currency_code6',
        'value0'
    )->build(),
    'opened_at0',
    'order_ref8',
    'reason8',
    'seller_response_due_date0',
    Status7Enum::NEEDS_REVIEW
)->build();
```



