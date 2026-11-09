# Post Disputes Case Ref Approve

Source: https://jiarong0423.github.io/payguard-ai/portal/#/ruby/x-redirect/JTI0ZSUyRm90aGVyJTJGcG9zdF9kaXNwdXRlc19jYXNlX3JlZl9hcHByb3Zl

Approve. Local console route POST /api/v1/disputes/{case_ref}/approve on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```ruby
def post_disputes_case_ref_approve(case_ref,
                                   body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `case_ref` | `String` | Template, Required | Case ref. |
| `body` | [`ApproveRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/approve-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`DisputeApprovalResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/structures/dispute-approval-response.md)


# Example Usage

```ruby
case_ref = 'case_ref4'

body = ApproveRequest.new(
  'draft_digest6'
)

result = other_controller.post_disputes_case_ref_approve(
  case_ref,
  body
)
puts result
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/ruby/models/exceptions/error-body.md) |



