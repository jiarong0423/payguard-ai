# Post Aup Acknowledge

Source: http://localhost:3000/#/ruby/x-redirect/JTI0ZSUyRmF1cCUyRnBvc3RfYXVwX2Fja25vd2xlZGdl

Acknowledge Aup. Local console route POST /api/v1/aup/acknowledge on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```ruby
def post_aup_acknowledge(body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`AupAcknowledgeRequest`](http://localhost:3000/llms-pages/ruby/models/structures/aup-acknowledge-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`AupAcknowledgeResponse`](http://localhost:3000/llms-pages/ruby/models/structures/aup-acknowledge-response.md)


# Example Usage

```ruby
body = AupAcknowledgeRequest.new(
  ChoiceEnum::CANCEL,
  'description_digest4',
  'evaluation_id0'
)

result = aup_controller.post_aup_acknowledge(body)
puts result
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/ruby/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](http://localhost:3000/llms-pages/ruby/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/ruby/models/exceptions/error-body.md) |



