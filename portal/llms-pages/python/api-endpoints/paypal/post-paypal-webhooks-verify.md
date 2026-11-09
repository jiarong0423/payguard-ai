# Post Paypal Webhooks Verify

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0ZSUyRnBheXBhbCUyRnBvc3RfcGF5cGFsX3dlYmhvb2tzX3ZlcmlmeQ

Verify Webhook. Local console route POST /api/v1/paypal/webhooks/verify on synthetic data; advisory only. The hosted demo answers 503 hosted_demo_disabled here: it makes no provider calls.

:information_source: **Note** This endpoint does not require authentication.

```python
def post_paypal_webhooks_verify(self)
```


# Response Type

**200**: Successful Response

[`WebhookVerifyResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/webhook-verify-response.md)


# Example Usage

```python
result = paypal_controller.post_paypal_webhooks_verify()
print(result)
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |



