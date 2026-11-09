# Post Cases Route

Source: http://localhost:3000/#/ruby/x-redirect/JTI0ZSUyRm90aGVyJTJGcG9zdF9jYXNlc19yb3V0ZQ

Case Route. Local console route POST /api/v1/cases/route on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```ruby
def post_cases_route(body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`CaseRouteRequest`](http://localhost:3000/llms-pages/ruby/models/structures/case-route-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`CaseRouteResponse`](http://localhost:3000/llms-pages/ruby/models/structures/case-route-response.md)


# Example Usage

```ruby
body = CaseRouteRequest.new(
  'text4'
)

result = other_controller.post_cases_route(body)
puts result
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/ruby/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](http://localhost:3000/llms-pages/ruby/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/ruby/models/exceptions/error-body.md) |



