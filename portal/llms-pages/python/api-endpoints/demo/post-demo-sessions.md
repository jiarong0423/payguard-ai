# Post Demo Sessions

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0ZSUyRmRlbW8lMkZwb3N0X2RlbW9fc2Vzc2lvbnM

New Session. Local console route POST /api/v1/demo/sessions on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```python
def post_demo_sessions(self,
                      body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | `Any` | Body, Required | - |


# Response Type

**201**: Successful Response

[`SessionResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/session-response.md)


# Example Usage

```python
body = jsonpickle.decode('{"key1":"val1","key2":"val2"}')

result = demo_controller.post_demo_sessions(body)
print(result)
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |



