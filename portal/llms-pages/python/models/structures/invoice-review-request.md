# Invoice Review Request

Source: http://localhost:3000/#/python/x-redirect/JTI0bSUyRkludm9pY2VSZXZpZXdSZXF1ZXN0

InvoiceReviewRequest.


# Class Name

`InvoiceReviewRequest`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `acknowledgement_token` | str \| None | Optional | This is a container for any-of cases. |
| `amount` | `str` | Required | Amount.<br><br>**Constraints**: *Pattern*: `^[0-9]{1,9}(?:\.[0-9]{1,2})?$` |
| `confirm_sandbox_draft` | `bool` | Required | Confirm sandbox draft. |
| `currency` | [`CurrencyEnum`](http://localhost:3000/llms-pages/python/models/enumerations/currency.md) | Required | Currency. |
| `description` | `str` | Required | Description.<br><br>**Constraints**: *Minimum Length*: `1`, *Maximum Length*: `200` |
| `description_digest` | str \| None | Optional | This is a container for any-of cases. |
| `evaluation_id` | str \| None | Optional | This is a container for any-of cases. |


# Example

```python
from tradeglotlocalconsole.models.currency_enum import CurrencyEnum
from tradeglotlocalconsole.models.invoice_review_request import InvoiceReviewRequest

invoice_review_request = InvoiceReviewRequest(
    amount='amount8',
    confirm_sandbox_draft=False,
    currency=CurrencyEnum.JPY,
    description='description0',
    acknowledgement_token='String1',
    description_digest='String9',
    evaluation_id='String7'
)
```



