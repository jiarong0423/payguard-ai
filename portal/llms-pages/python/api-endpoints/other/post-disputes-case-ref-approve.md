# Post Disputes Case Ref Approve

Source: http://localhost:3000/#/python/x-redirect/JTI0ZSUyRm90aGVyJTJGcG9zdF9kaXNwdXRlc19jYXNlX3JlZl9hcHByb3Zl

Approve. Local console route POST /api/v1/disputes/{case_ref}/approve on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```python
def post_disputes_case_ref_approve(self,
                                  case_ref,
                                  body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `case_ref` | `str` | Template, Required | Case ref. |
| `body` | [`ApproveRequest`](http://localhost:3000/llms-pages/python/models/structures/approve-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`DisputeApprovalResponse`](http://localhost:3000/llms-pages/python/models/structures/dispute-approval-response.md)


# Example Usage

```python
case_ref = 'case_ref4'

body = ApproveRequest(
    draft_digest='draft_digest6'
)

result = other_controller.post_disputes_case_ref_approve(
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



