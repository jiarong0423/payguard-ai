# Get Health

Source: http://localhost:3000/#/python/x-redirect/JTI0ZSUyRmhlYWx0aCUyRmdldF9oZWFsdGg

Health. Local console route GET /api/v1/health on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```python
def get_health(self)
```


# Response Type

**200**: Successful Response

[`HealthResponse`](http://localhost:3000/llms-pages/python/models/structures/health-response.md)


# Example Usage

```python
result = health_controller.get_health()
print(result)
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/python/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/python/models/exceptions/error-body.md) |



