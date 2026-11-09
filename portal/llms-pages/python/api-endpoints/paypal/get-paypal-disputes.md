# Get Paypal Disputes

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0ZSUyRnBheXBhbCUyRmdldF9wYXlwYWxfZGlzcHV0ZXM

List Disputes. Local console route GET /api/v1/paypal/disputes on synthetic data; advisory only.

```python
def get_paypal_disputes(self)
```


# Authentication

This endpoint requires [DemoSession](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/getting-started/how-to-get-started/authorization.md)


# Response Type

**200**: Successful Response

[`DisputeListResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/dispute-list-response.md)


# Example Usage

```python
result = paypal_controller.get_paypal_disputes()
print(result)
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |



