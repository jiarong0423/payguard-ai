# Post Paypal Invoices Review

Source: http://localhost:3000/#/python/x-redirect/JTI0ZSUyRnBheXBhbCUyRnBvc3RfcGF5cGFsX2ludm9pY2VzX3Jldmlldw

Invoice Review. Local console route POST /api/v1/paypal/invoices/review on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```python
def post_paypal_invoices_review(self,
                               body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`InvoiceReviewRequest`](http://localhost:3000/llms-pages/python/models/structures/invoice-review-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`InvoiceReviewResponse`](http://localhost:3000/llms-pages/python/models/structures/invoice-review-response.md)


# Example Usage

```python
body = InvoiceReviewRequest(
    amount='amount8',
    confirm_sandbox_draft=False,
    currency=CurrencyEnum.USD,
    description='description4'
)

result = paypal_controller.post_paypal_invoices_review(body)
print(result)
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/python/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](http://localhost:3000/llms-pages/python/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/python/models/exceptions/error-body.md) |



