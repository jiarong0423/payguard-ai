# Post Aup Category Signal

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0ZSUyRmF1cCUyRnBvc3RfYXVwX2NhdGVnb3J5X3NpZ25hbA

Aup Category Signal. Local console route POST /api/v1/aup/category-signal on synthetic data; advisory only.

```ruby
def post_aup_category_signal(body)
```


# Authentication

This endpoint requires [DemoCsrf](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/getting-started/how-to-get-started/authorization.md) **AND** [DemoSession](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/getting-started/how-to-get-started/authorization.md)


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`AupCategorySignalRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/aup-category-signal-request.md) | Body, Required | JSON body for: Aup Category Signal. |


# Response Type

**200**: Successful Response

[`AupCategorySignalResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/aup-category-signal-response.md)


# Example Usage

```ruby
body = AupCategorySignalRequest.new(
  'example',
  'examplexxxxxxxxxxxxxxxxxxxxxxxxx'
)

result = aup_controller.post_aup_category_signal(body)
puts result
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/error-body.md) |
| 403 | Origin missing or not allowed, or the CSRF token is wrong (origin_required, origin_rejected, csrf_rejected). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/error-body.md) |
| 422 | The request does not match the accepted contract (schema_invalid). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/error-body.md) |



