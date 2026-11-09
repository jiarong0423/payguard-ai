# Post Guide Review

Source: http://localhost:3000/#/python/x-redirect/JTI0ZSUyRmd1aWRlJTJGcG9zdF9ndWlkZV9yZXZpZXc

Guide Review. Local console route POST /api/v1/guide/review on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```python
def post_guide_review(self,
                     body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`GuideReviewRequest`](http://localhost:3000/llms-pages/python/models/structures/guide-review-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`GuideStateResponse`](http://localhost:3000/llms-pages/python/models/structures/guide-state-response.md)


# Example Usage

```python
body = GuideReviewRequest(
    confirm=False
)

result = guide_controller.post_guide_review(body)
print(result)
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/python/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](http://localhost:3000/llms-pages/python/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/python/models/exceptions/error-body.md) |



