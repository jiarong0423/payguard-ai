# Post Aup Review

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0ZSUyRmF1cCUyRnBvc3RfYXVwX3Jldmlldw

Aup. Local console route POST /api/v1/aup/review on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```ruby
def post_aup_review(body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`AupRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/aup-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`AupResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/aup-response.md)


# Example Usage

```ruby
body = AupRequest.new(
  'description4'
)

result = aup_controller.post_aup_review(body)
puts result
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/error-body.md) |



