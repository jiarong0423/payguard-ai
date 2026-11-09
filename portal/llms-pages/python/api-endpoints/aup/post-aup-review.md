# Post Aup Review

Source: http://localhost:3000/#/python/x-redirect/JTI0ZSUyRmF1cCUyRnBvc3RfYXVwX3Jldmlldw

Aup. Local console route POST /api/v1/aup/review on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```python
def post_aup_review(self,
                   body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`AupRequest`](http://localhost:3000/llms-pages/python/models/structures/aup-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`AupResponse`](http://localhost:3000/llms-pages/python/models/structures/aup-response.md)


# Example Usage

```python
body = AupRequest(
    description='description4'
)

result = aup_controller.post_aup_review(body)
print(result)
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/python/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](http://localhost:3000/llms-pages/python/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/python/models/exceptions/error-body.md) |



