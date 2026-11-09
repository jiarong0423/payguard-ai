# Post Disputes Case Ref Approve

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0ZSUyRm90aGVyJTJGcG9zdF9kaXNwdXRlc19jYXNlX3JlZl9hcHByb3Zl

Approve. Local console route POST /api/v1/disputes/{case_ref}/approve on synthetic data; advisory only.

```java
CompletableFuture<DisputeApprovalResponse> postDisputesCaseRefApproveAsync(
    final String caseRef,
    final ApproveRequest body)
```


# Authentication

This endpoint requires [DemoCsrf](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/getting-started/how-to-get-started/authorization.md) **AND** [DemoSession](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/getting-started/how-to-get-started/authorization.md)


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `caseRef` | `String` | Template, Required | Case ref. |
| `body` | [`ApproveRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/approve-request.md) | Body, Required | JSON body for: Approve. |


# Response Type

**200**: Successful Response

[`DisputeApprovalResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/dispute-approval-response.md)


# Example Usage

```java
String caseRef = "case-ref-001";
ApproveRequest body = new ApproveRequest.Builder(
    "draft_digest6"
)
.build();

otherController.postDisputesCaseRefApproveAsync(caseRef, body).thenAccept(result -> {
    // TODO success callback handler
    System.out.println(result);
}).exceptionally(exception -> {
    Throwable cause = exception.getCause();

    if (cause instanceof ErrorBodyException) {
        ErrorBodyException errorBodyException = (ErrorBodyException) cause;
        errorBodyException.printStackTrace();
    } else {
        // fallback for unexpected errors
        exception.printStackTrace();
    }

    return null;
});
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/exceptions/error-body.md) |
| 403 | Origin missing or not allowed, or the CSRF token is wrong (origin_required, origin_rejected, csrf_rejected). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/exceptions/error-body.md) |
| 422 | The request does not match the accepted contract (schema_invalid). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/exceptions/error-body.md) |



