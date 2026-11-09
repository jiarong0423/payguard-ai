# Post Advisory Evaluate

Source: http://localhost:3000/#/ruby/x-redirect/JTI0ZSUyRm90aGVyJTJGcG9zdF9hZHZpc29yeV9ldmFsdWF0ZQ

Advisory Evaluate. Local console route POST /api/v1/advisory/evaluate on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```ruby
def post_advisory_evaluate(body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`AdvisoryRequest`](http://localhost:3000/llms-pages/ruby/models/structures/advisory-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`AdvisoryEvaluationResponse`](http://localhost:3000/llms-pages/ruby/models/structures/advisory-evaluation-response.md)


# Example Usage

```ruby
body = AdvisoryRequest.new(
  'as_of2',
  'candidate_json2',
  'US',
  102,
  ThemeEnum::DISPUTE_MEDIATION
)

result = other_controller.post_advisory_evaluate(body)
puts result
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/ruby/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](http://localhost:3000/llms-pages/ruby/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/ruby/models/exceptions/error-body.md) |



