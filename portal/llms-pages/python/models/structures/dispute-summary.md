# Dispute Summary

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkRpc3B1dGVTdW1tYXJ5

DisputeSummary.


# Class Name

`DisputeSummary`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `case_ref` | `str` | Required | Case ref. |
| `dispute_amount` | [`SyntheticMoney`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/synthetic-money.md) | Required | Same shape as the PayPal Disputes `dispute_amount` (ProviderMoney below); values are synthetic. |
| `opened_at` | `str` | Required | Opened at. |
| `order_ref` | `str` | Required | Order ref. |
| `reason` | `str` | Required | Reason. |
| `seller_response_due_date` | `str` | Required | Seller response due date. |
| `status` | [`Status7Enum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/status-7.md) | Required | Status. |


# Example

```python
from tradeglotlocalconsole.models.dispute_summary import DisputeSummary
from tradeglotlocalconsole.models.status_7_enum import Status7Enum
from tradeglotlocalconsole.models.synthetic_money import SyntheticMoney

dispute_summary = DisputeSummary(
    case_ref='case_ref6',
    dispute_amount=SyntheticMoney(
        currency_code='currency_code6',
        value='value0'
    ),
    opened_at='opened_at0',
    order_ref='order_ref8',
    reason='reason8',
    seller_response_due_date='seller_response_due_date0',
    status=Status7Enum.LOCAL_DRAFT_REVIEWED
)
```



