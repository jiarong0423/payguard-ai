# Post Aup Category Signal

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0ZSUyRmF1cCUyRnBvc3RfYXVwX2NhdGVnb3J5X3NpZ25hbA

Aup Category Signal. Local console route POST /api/v1/aup/category-signal on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```ruby
def post_aup_category_signal(body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`AupCategorySignalRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/aup-category-signal-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`AupCategorySignalResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/aup-category-signal-response.md)


# Example Usage

```ruby
body = AupCategorySignalRequest.new(
  'description4',
  'evaluation_id0'
)

result = aup_controller.post_aup_category_signal(body)
puts result
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/error-body.md) |



