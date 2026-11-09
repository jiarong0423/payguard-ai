# Post Paypal Disputes Add Tracking

Source: http://localhost:3000/#/python/x-redirect/JTI0ZSUyRnBheXBhbCUyRnBvc3RfcGF5cGFsX2Rpc3B1dGVzX2FkZF90cmFja2luZw

Add Tracking. Local console route POST /api/v1/paypal/disputes/add-tracking on synthetic data; advisory only. The hosted demo answers 503 hosted_demo_disabled here: it makes no provider calls.

:information_source: **Note** This endpoint does not require authentication.

```python
def post_paypal_disputes_add_tracking(self,
                                     body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`AddTrackingRequest`](http://localhost:3000/llms-pages/python/models/structures/add-tracking-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`AddTrackingResponse`](http://localhost:3000/llms-pages/python/models/structures/add-tracking-response.md)


# Example Usage

```python
body = AddTrackingRequest(
    case_ref='case_ref0',
    dispute_id='dispute_id8',
    submit=False
)

result = paypal_controller.post_paypal_disputes_add_tracking(body)
print(result)
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/python/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](http://localhost:3000/llms-pages/python/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/python/models/exceptions/error-body.md) |



