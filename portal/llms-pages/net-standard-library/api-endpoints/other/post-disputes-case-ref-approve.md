# Post Disputes Case Ref Approve

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0ZSUyRm90aGVyJTJGcG9zdF9kaXNwdXRlc19jYXNlX3JlZl9hcHByb3Zl

Approve. Local console route POST /api/v1/disputes/{case_ref}/approve on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```csharp
PostDisputesCaseRefApproveAsync(
    string caseRef,
    Models.ApproveRequest body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `caseRef` | `string` | Template, Required | Case ref. |
| `body` | [`ApproveRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/approve-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`Task<Models.DisputeApprovalResponse>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/dispute-approval-response.md)


# Example Usage

```csharp
string caseRef = "case_ref4";
ApproveRequest body = new ApproveRequest
{
    DraftDigest = "draft_digest6",
};

try
{
    DisputeApprovalResponse result = await otherController.PostDisputesCaseRefApproveAsync(
        caseRef,
        body
    );
}
catch (ApiException e)
{
    Console.WriteLine(e.Message);
    if (e is ErrorBodyException)
    {
       // TODO: Handle ErrorBodyException exception here
    }
    if (e is HTTPValidationErrorException)
    {
       // TODO: Handle HTTPValidationErrorException exception here
    }
}
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/exceptions/error-body.md) |



