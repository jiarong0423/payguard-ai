# Post References Search

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0ZSUyRnJlZmVyZW5jZXMlMkZwb3N0X3JlZmVyZW5jZXNfc2VhcmNo

References. Local console route POST /api/v1/references/search on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```python
def post_references_search(self,
                          body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`ReferenceRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/reference-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`ReferenceResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/reference-response.md)


# Example Usage

```python
body = ReferenceRequest(
    query='query6',
    theme=ThemeEnum.DISPUTE_MEDIATION,
    case_stage=CaseStage2Enum.ANY,
    limit=3,
    require_known_source_date=False
)

result = references_controller.post_references_search(body)
print(result)
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |



