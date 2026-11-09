# Post Paypal Webhooks Verify

Source: http://localhost:3000/#/ruby/x-redirect/JTI0ZSUyRnBheXBhbCUyRnBvc3RfcGF5cGFsX3dlYmhvb2tzX3ZlcmlmeQ

Verify Webhook. Local console route POST /api/v1/paypal/webhooks/verify on synthetic data; advisory only. The hosted demo answers 503 hosted_demo_disabled here: it makes no provider calls.

:information_source: **Note** This endpoint does not require authentication.

```ruby
def post_paypal_webhooks_verify
```


# Response Type

**200**: Successful Response

[`WebhookVerifyResponse`](http://localhost:3000/llms-pages/ruby/models/structures/webhook-verify-response.md)


# Example Usage

```ruby
result = paypal_controller.post_paypal_webhooks_verify
puts result
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/ruby/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/ruby/models/exceptions/error-body.md) |



