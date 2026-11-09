# Post Paypal Invoices Draft

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0ZSUyRnBheXBhbCUyRnBvc3RfcGF5cGFsX2ludm9pY2VzX2RyYWZ0

Invoice Draft. Local console route POST /api/v1/paypal/invoices/draft on synthetic data; advisory only. The hosted demo answers 503 hosted_demo_disabled here: it makes no provider calls.

```python
def post_paypal_invoices_draft(self,
                              body)
```


# Authentication

This endpoint requires [DemoCsrf](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/getting-started/how-to-get-started/authorization.md) **AND** [DemoSession](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/getting-started/how-to-get-started/authorization.md)


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`InvoiceDraftRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/invoice-draft-request.md) | Body, Required | JSON body for: Invoice Draft. |


# Response Type

**200**: Successful Response

[`InvoiceDraftResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/invoice-draft-response.md)


# Example Usage

```python
body = InvoiceDraftRequest(
    amount='amount8',
    currency=CurrencyEnum.USD,
    description='description4',
    payload_digest='payload_digest4',
    review_token='review_token4'
)

result = paypal_controller.post_paypal_invoices_draft(body)
print(result)
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |
| 403 | Origin missing or not allowed, or the CSRF token is wrong (origin_required, origin_rejected, csrf_rejected). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |
| 422 | The request does not match the accepted contract (schema_invalid). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |
| 503 | Hosted demo only: this route makes no provider call (hosted_demo_disabled). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |



