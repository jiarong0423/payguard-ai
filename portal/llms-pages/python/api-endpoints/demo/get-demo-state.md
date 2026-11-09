# Get Demo State

Source: http://localhost:3000/#/python/x-redirect/JTI0ZSUyRmRlbW8lMkZnZXRfZGVtb19zdGF0ZQ

State. Local console route GET /api/v1/demo/state on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```python
def get_demo_state(self)
```


# Response Type

**200**: Successful Response

[`StateResponse`](http://localhost:3000/llms-pages/python/models/structures/state-response.md)


# Example Usage

```python
result = demo_controller.get_demo_state()
print(result)
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/python/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/python/models/exceptions/error-body.md) |



