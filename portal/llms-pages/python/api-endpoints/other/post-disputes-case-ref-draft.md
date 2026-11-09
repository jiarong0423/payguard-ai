# Post Disputes Case Ref Draft

Source: http://localhost:3000/#/python/x-redirect/JTI0ZSUyRm90aGVyJTJGcG9zdF9kaXNwdXRlc19jYXNlX3JlZl9kcmFmdA

Draft. Local console route POST /api/v1/disputes/{case_ref}/draft on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```python
def post_disputes_case_ref_draft(self,
                                case_ref,
                                body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `case_ref` | `str` | Template, Required | Case ref. |
| `body` | `Any` | Body, Required | - |


# Response Type

**200**: Successful Response

[`DisputeDraftResponse`](http://localhost:3000/llms-pages/python/models/structures/dispute-draft-response.md)


# Example Usage

```python
case_ref = 'case_ref4'

body = jsonpickle.decode('{"key1":"val1","key2":"val2"}')

result = other_controller.post_disputes_case_ref_draft(
    case_ref,
    body
)
print(result)
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/python/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](http://localhost:3000/llms-pages/python/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/python/models/exceptions/error-body.md) |



