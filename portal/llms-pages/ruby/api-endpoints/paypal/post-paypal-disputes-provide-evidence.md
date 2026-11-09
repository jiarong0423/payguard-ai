# Post Paypal Disputes Provide Evidence

Source: http://localhost:3000/#/ruby/x-redirect/JTI0ZSUyRnBheXBhbCUyRnBvc3RfcGF5cGFsX2Rpc3B1dGVzX3Byb3ZpZGVfZXZpZGVuY2U

Provide Evidence. Local console route POST /api/v1/paypal/disputes/provide-evidence on synthetic data; advisory only. The hosted demo answers 503 hosted_demo_disabled here: it makes no provider calls.

:information_source: **Note** This endpoint does not require authentication.

```ruby
def post_paypal_disputes_provide_evidence(body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`ProvideEvidenceRequest`](http://localhost:3000/llms-pages/ruby/models/structures/provide-evidence-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`ProvideEvidenceResponse`](http://localhost:3000/llms-pages/ruby/models/structures/provide-evidence-response.md)


# Example Usage

```ruby
body = ProvideEvidenceRequest.new(
  'case_ref0',
  'dispute_id8',
  nil,
  false
)

result = paypal_controller.post_paypal_disputes_provide_evidence(body)
puts result
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/ruby/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](http://localhost:3000/llms-pages/ruby/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/ruby/models/exceptions/error-body.md) |



