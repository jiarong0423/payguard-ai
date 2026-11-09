# Get Paypal Status

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0ZSUyRnBheXBhbCUyRmdldF9wYXlwYWxfc3RhdHVz

Paypal Status. Local console route GET /api/v1/paypal/status on synthetic data; advisory only.

```ruby
def get_paypal_status
```


# Authentication

This endpoint requires [DemoSession](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/getting-started/how-to-get-started/authorization.md)


# Response Type

**200**: Successful Response

[`PaypalStatusResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/paypal-status-response.md)


# Example Usage

```ruby
result = paypal_controller.get_paypal_status
puts result
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/error-body.md) |



