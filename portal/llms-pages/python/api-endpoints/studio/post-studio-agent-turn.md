# Post Studio Agent Turn

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0ZSUyRnN0dWRpbyUyRnBvc3Rfc3R1ZGlvX2FnZW50X3R1cm4

Studio Agent Turn. Local console route POST /api/v1/studio/agent-turn on synthetic data; advisory only. The hosted demo answers 503 hosted_demo_disabled here: it makes no provider calls.

:information_source: **Note** This endpoint does not require authentication.

```python
def post_studio_agent_turn(self,
                          body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | `Any` | Body, Required | - |


# Response Type

**200**: Successful Response

`Any`


# Example Usage

```python
body = jsonpickle.decode('{"key1":"val1","key2":"val2"}')

result = studio_controller.post_studio_agent_turn(body)
print(result)
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |



