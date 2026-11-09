# Dispute Summary

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0bSUyRkRpc3B1dGVTdW1tYXJ5

DisputeSummary.


# Class Name

`DisputeSummary`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `case_ref` | `String` | Required | Case ref. |
| `dispute_amount` | [`SyntheticMoney`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/synthetic-money.md) | Required | Same shape as the PayPal Disputes `dispute_amount` (ProviderMoney below); values are synthetic. |
| `opened_at` | `String` | Required | Opened at. |
| `order_ref` | `String` | Required | Order ref. |
| `reason` | `String` | Required | Reason. |
| `seller_response_due_date` | `String` | Required | Seller response due date. |
| `status` | [`Status7Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/enumerations/status-7.md) | Required | Status. |


# Example

```ruby
dispute_summary = DisputeSummary.new(
  'case_ref6',
  SyntheticMoney.new(
    'currency_code6',
    'value0'
  ),
  'opened_at0',
  'order_ref8',
  'reason8',
  'seller_response_due_date0',
  Status7Enum::LOCAL_DRAFT_REVIEWED
)
```



