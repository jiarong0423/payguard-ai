# Post Country Rules Search

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0ZSUyRm90aGVyJTJGcG9zdF9jb3VudHJ5X3J1bGVzX3NlYXJjaA

Country Rules Search. Local console route POST /api/v1/country-rules/search on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```python
def post_country_rules_search(self,
                             body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`CountryRulesSearchRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/country-rules-search-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

`Any`


# Example Usage

```python
body = CountryRulesSearchRequest(
    query='query6',
    limit=5
)

result = other_controller.post_country_rules_search(body)
print(result)
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |



