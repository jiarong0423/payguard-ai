# Get Paypal Disputes

Source: http://localhost:3000/#/python/x-redirect/JTI0ZSUyRnBheXBhbCUyRmdldF9wYXlwYWxfZGlzcHV0ZXM

List Disputes. Local console route GET /api/v1/paypal/disputes on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```python
def get_paypal_disputes(self)
```


# Response Type

**200**: Successful Response

[`DisputeListResponse`](http://localhost:3000/llms-pages/python/models/structures/dispute-list-response.md)


# Example Usage

```python
result = paypal_controller.get_paypal_disputes()
print(result)
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/python/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/python/models/exceptions/error-body.md) |



