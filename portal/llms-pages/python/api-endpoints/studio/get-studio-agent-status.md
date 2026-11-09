# Get Studio Agent Status

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0ZSUyRnN0dWRpbyUyRmdldF9zdHVkaW9fYWdlbnRfc3RhdHVz

Studio Agent Status. Local console route GET /api/v1/studio/agent-status on synthetic data; advisory only.

```python
def get_studio_agent_status(self)
```


# Authentication

This endpoint requires [DemoSession](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/getting-started/how-to-get-started/authorization.md)


# Response Type

**200**: Successful Response

`Any`


# Example Usage

```python
result = studio_controller.get_studio_agent_status()
print(result)
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |



