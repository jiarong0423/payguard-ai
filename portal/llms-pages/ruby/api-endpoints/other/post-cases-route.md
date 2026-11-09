# Post Cases Route

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0ZSUyRm90aGVyJTJGcG9zdF9jYXNlc19yb3V0ZQ

Case Route. Local console route POST /api/v1/cases/route on synthetic data; advisory only.

```ruby
def post_cases_route(body)
```


# Authentication

This endpoint requires [DemoCsrf](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/getting-started/how-to-get-started/authorization.md) **AND** [DemoSession](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/getting-started/how-to-get-started/authorization.md)


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`CaseRouteRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/case-route-request.md) | Body, Required | JSON body for: Case Route. |


# Response Type

**200**: Successful Response

[`CaseRouteResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/case-route-response.md)


# Example Usage

```ruby
body = CaseRouteRequest.new(
  'handmade ceramic coffee mug'
)

result = other_controller.post_cases_route(body)
puts result
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/error-body.md) |
| 403 | Origin missing or not allowed, or the CSRF token is wrong (origin_required, origin_rejected, csrf_rejected). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/error-body.md) |
| 422 | The request does not match the accepted contract (schema_invalid). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/error-body.md) |



