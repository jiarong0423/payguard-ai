# Get Connections

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0ZSUyRm90aGVyJTJGZ2V0X2Nvbm5lY3Rpb25z

Connections. Local console route GET /api/v1/connections on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```python
def get_connections(self)
```


# Response Type

**200**: Successful Response

[`ConnectionsResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/connections-response.md)


# Example Usage

```python
result = other_controller.get_connections()
print(result)
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |



