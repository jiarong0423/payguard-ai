# Post Aup Review

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0ZSUyRmF1cCUyRnBvc3RfYXVwX3Jldmlldw

Aup. Local console route POST /api/v1/aup/review on synthetic data; advisory only.

```python
def post_aup_review(self,
                   body)
```


# Authentication

This endpoint requires [DemoCsrf](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/getting-started/how-to-get-started/authorization.md) **AND** [DemoSession](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/getting-started/how-to-get-started/authorization.md)


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`AupRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/aup-request.md) | Body, Required | JSON body for: Aup. |


# Response Type

**200**: Successful Response

[`AupResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/aup-response.md)


# Example Usage

```python
body = AupRequest(
    description='Handmade ceramic coffee mug, shipped in a padded box'
)

result = aup_controller.post_aup_review(body)
print(result)
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |
| 403 | Origin missing or not allowed, or the CSRF token is wrong (origin_required, origin_rejected, csrf_rejected). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |
| 422 | The request does not match the accepted contract (schema_invalid). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |



