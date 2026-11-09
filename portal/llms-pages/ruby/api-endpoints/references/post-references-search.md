# Post References Search

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0ZSUyRnJlZmVyZW5jZXMlMkZwb3N0X3JlZmVyZW5jZXNfc2VhcmNo

References. Local console route POST /api/v1/references/search on synthetic data; advisory only.

```ruby
def post_references_search(body)
```


# Authentication

This endpoint requires [DemoCsrf](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/getting-started/how-to-get-started/authorization.md) **AND** [DemoSession](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/getting-started/how-to-get-started/authorization.md)


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`ReferenceRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/reference-request.md) | Body, Required | JSON body for: References. |


# Response Type

**200**: Successful Response

[`ReferenceResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/reference-response.md)


# Example Usage

```ruby
body = ReferenceRequest.new(
  'US',
  'example',
  ThemeEnum::SOURCE_COMPLIANCE,
  nil,
  envrr
)

result = references_controller.post_references_search(body)
puts result
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/error-body.md) |
| 403 | Origin missing or not allowed, or the CSRF token is wrong (origin_required, origin_rejected, csrf_rejected). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/error-body.md) |
| 422 | The request does not match the accepted contract (schema_invalid). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/error-body.md) |



