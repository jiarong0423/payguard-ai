# Post Demo Inject

Source: http://localhost:3000/#/ruby/x-redirect/JTI0ZSUyRmRlbW8lMkZwb3N0X2RlbW9faW5qZWN0

Inject. Local console route POST /api/v1/demo/inject on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```ruby
def post_demo_inject(body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`InjectRequest`](http://localhost:3000/llms-pages/ruby/models/structures/inject-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`StateResponse`](http://localhost:3000/llms-pages/ruby/models/structures/state-response.md)


# Example Usage

```ruby
body = InjectRequest.new(
  Scenario5Enum::DISPUTE
)

result = demo_controller.post_demo_inject(body)
puts result
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/ruby/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](http://localhost:3000/llms-pages/ruby/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/ruby/models/exceptions/error-body.md) |



