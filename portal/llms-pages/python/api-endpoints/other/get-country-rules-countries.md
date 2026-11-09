# Get Country Rules Countries

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0ZSUyRm90aGVyJTJGZ2V0X2NvdW50cnlfcnVsZXNfY291bnRyaWVz

Country Rules Countries. Local console route GET /api/v1/country-rules/countries on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```python
def get_country_rules_countries(self)
```


# Response Type

**200**: Successful Response

`Any`


# Example Usage

```python
result = other_controller.get_country_rules_countries()
print(result)
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |



