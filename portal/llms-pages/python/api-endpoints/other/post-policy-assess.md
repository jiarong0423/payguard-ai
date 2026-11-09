# Post Policy Assess

Source: http://localhost:3000/#/python/x-redirect/JTI0ZSUyRm90aGVyJTJGcG9zdF9wb2xpY3lfYXNzZXNz

Policy Assess. Local console route POST /api/v1/policy/assess on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```python
def post_policy_assess(self,
                      body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`PolicyRequest`](http://localhost:3000/llms-pages/python/models/structures/policy-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`PolicyAssessmentResponse`](http://localhost:3000/llms-pages/python/models/structures/policy-assessment-response.md)


# Example Usage

```python
body = PolicyRequest(
    as_of='as_of2',
    observation_max_age_days=102,
    theme=ThemeEnum.DISPUTE_MEDIATION
)

result = other_controller.post_policy_assess(body)
print(result)
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/python/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](http://localhost:3000/llms-pages/python/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/python/models/exceptions/error-body.md) |



