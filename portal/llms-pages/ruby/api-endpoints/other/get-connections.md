# Get Connections

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0ZSUyRm90aGVyJTJGZ2V0X2Nvbm5lY3Rpb25z

Connections. Local console route GET /api/v1/connections on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```ruby
def get_connections
```


# Response Type

**200**: Successful Response

[`ConnectionsResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/connections-response.md)


# Example Usage

```ruby
result = other_controller.get_connections
puts result
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/error-body.md) |



