# Post Guide Form

Source: http://localhost:3000/#/ruby/x-redirect/JTI0ZSUyRmd1aWRlJTJGcG9zdF9ndWlkZV9mb3Jt

Guide Form. Local console route POST /api/v1/guide/form on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```ruby
def post_guide_form(body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`GuideFormRequest`](http://localhost:3000/llms-pages/ruby/models/structures/guide-form-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`GuideStateResponse`](http://localhost:3000/llms-pages/ruby/models/structures/guide-state-response.md)


# Example Usage

```ruby
body = GuideFormRequest.new(
  false
)

result = guide_controller.post_guide_form(body)
puts result
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/ruby/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](http://localhost:3000/llms-pages/ruby/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/ruby/models/exceptions/error-body.md) |



