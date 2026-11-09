# Post Cases Route

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0ZSUyRm90aGVyJTJGcG9zdF9jYXNlc19yb3V0ZQ

Case Route. Local console route POST /api/v1/cases/route on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```python
def post_cases_route(self,
                    body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`CaseRouteRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/case-route-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`CaseRouteResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/case-route-response.md)


# Example Usage

```python
body = CaseRouteRequest(
    text='text4'
)

result = other_controller.post_cases_route(body)
print(result)
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |



