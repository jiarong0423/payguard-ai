# Invoice Draft Request

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkludm9pY2VEcmFmdFJlcXVlc3Q

InvoiceDraftRequest.


# Class Name

`InvoiceDraftRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `amount` | `str` | Required | Amount.<br><br>**Constraints**: *Pattern*: `^[0-9]{1,9}(?:\.[0-9]{1,2})?$` |
| `currency` | [`CurrencyEnum`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/enumerations/currency.md) | Required | Currency. |
| `description` | `str` | Required | Description.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `200` |
| `payload_digest` | `str` | Required | Payload digest.<br><br>**Constraints**: *Pattern*: `^[a-f0-9]{64}$` |
| `review_token` | `str` | Required | Review token.<br><br>**Constraints**: *Minimum Length*: `32`, *Maximum Length*: `128` |


# Example

```python
from tradeglotlocalconsole.models.currency_enum import CurrencyEnum
from tradeglotlocalconsole.models.invoice_draft_request import InvoiceDraftRequest

invoice_draft_request = InvoiceDraftRequest(
    amount='amount4',
    currency=CurrencyEnum.JPY,
    description='description2',
    payload_digest='payload_digest2',
    review_token='review_token0'
)
```



