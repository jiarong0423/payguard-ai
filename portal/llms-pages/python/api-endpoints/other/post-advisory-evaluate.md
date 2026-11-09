# Post Advisory Evaluate

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0ZSUyRm90aGVyJTJGcG9zdF9hZHZpc29yeV9ldmFsdWF0ZQ

Advisory Evaluate. Local console route POST /api/v1/advisory/evaluate on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```python
def post_advisory_evaluate(self,
                          body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`AdvisoryRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/advisory-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`AdvisoryEvaluationResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/advisory-evaluation-response.md)


# Example Usage

```python
body = AdvisoryRequest(
    as_of='as_of2',
    candidate_json='candidate_json2',
    observation_max_age_days=102,
    theme=ThemeEnum.DISPUTE_MEDIATION
)

result = other_controller.post_advisory_evaluate(body)
print(result)
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |



