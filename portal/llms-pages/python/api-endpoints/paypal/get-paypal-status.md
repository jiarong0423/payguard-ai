# Get Paypal Status

Source: http://localhost:3000/#/python/x-redirect/JTI0ZSUyRnBheXBhbCUyRmdldF9wYXlwYWxfc3RhdHVz

Paypal Status. Local console route GET /api/v1/paypal/status on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```python
def get_paypal_status(self)
```


# Response Type

**200**: Successful Response

[`PaypalStatusResponse`](http://localhost:3000/llms-pages/python/models/structures/paypal-status-response.md)


# Example Usage

```python
result = paypal_controller.get_paypal_status()
print(result)
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/python/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/python/models/exceptions/error-body.md) |



