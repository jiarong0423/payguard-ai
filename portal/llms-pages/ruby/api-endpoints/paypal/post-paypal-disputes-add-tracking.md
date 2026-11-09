# Post Paypal Disputes Add Tracking

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0ZSUyRnBheXBhbCUyRnBvc3RfcGF5cGFsX2Rpc3B1dGVzX2FkZF90cmFja2luZw

Add Tracking. Local console route POST /api/v1/paypal/disputes/add-tracking on synthetic data; advisory only. The hosted demo answers 503 hosted_demo_disabled here: it makes no provider calls.

:information_source: **Note** This endpoint does not require authentication.

```ruby
def post_paypal_disputes_add_tracking(body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`AddTrackingRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/add-tracking-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`AddTrackingResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/add-tracking-response.md)


# Example Usage

```ruby
body = AddTrackingRequest.new(
  'case_ref0',
  'dispute_id8',
  nil,
  false
)

result = paypal_controller.post_paypal_disputes_add_tracking(body)
puts result
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/error-body.md) |



