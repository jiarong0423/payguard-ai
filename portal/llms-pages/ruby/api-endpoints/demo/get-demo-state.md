# Get Demo State

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0ZSUyRmRlbW8lMkZnZXRfZGVtb19zdGF0ZQ

State. Local console route GET /api/v1/demo/state on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```ruby
def get_demo_state
```


# Response Type

**200**: Successful Response

[`StateResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/state-response.md)


# Example Usage

```ruby
result = demo_controller.get_demo_state
puts result
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/error-body.md) |



