# Invoice Review Response

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0bSUyRkludm9pY2VSZXZpZXdSZXNwb25zZQ

InvoiceReviewResponse.


# Class Name

`InvoiceReviewResponse`


# Fields

| Name | Type | Tags | Description |
|  --- | --- | --- | --- |
| `action` | `str` | Required, Constant | Action.<br><br>**Value**: `"create_sandbox_invoice_draft"` |
| `advisory_only` | `str` | Required, Constant | Advisory only.<br><br>**Value**: `"True"` |
| `authenticated_actor` | `str` | Required, Constant | Authenticated actor.<br><br>**Value**: `"False"` |
| `expires_at` | `str` | Required | Expires at. |
| `limitations` | `List[str]` | Required | Limitations. |
| `payload_digest` | `str` | Required | Payload digest. |
| `policy_status` | `str` | Required, Constant | Policy status.<br><br>**Value**: `"manual_review"` |
| `review_token` | `str` | Required | Review token. |
| `source` | `str` | Required, Constant | Source.<br><br>**Value**: `"synthetic"` |


# Example

```python
from tradeglotlocalconsole.models.invoice_review_response import InvoiceReviewResponse

invoice_review_response = InvoiceReviewResponse(
    expires_at='expires_at4',
    limitations=[
        'limitations9'
    ],
    payload_digest='payload_digest2',
    review_token='review_token0'
)
```



