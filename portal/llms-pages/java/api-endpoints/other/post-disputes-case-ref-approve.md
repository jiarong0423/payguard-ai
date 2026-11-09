# Post Disputes Case Ref Approve

Source: http://localhost:3000/#/java/x-redirect/JTI0ZSUyRm90aGVyJTJGcG9zdF9kaXNwdXRlc19jYXNlX3JlZl9hcHByb3Zl

Approve. Local console route POST /api/v1/disputes/{case_ref}/approve on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```java
CompletableFuture<DisputeApprovalResponse> postDisputesCaseRefApproveAsync(
    final String caseRef,
    final ApproveRequest body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `caseRef` | `String` | Template, Required | Case ref. |
| `body` | [`ApproveRequest`](http://localhost:3000/llms-pages/java/models/structures/approve-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`DisputeApprovalResponse`](http://localhost:3000/llms-pages/java/models/structures/dispute-approval-response.md)


# Example Usage

```java
String caseRef = "case_ref4";
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
    } else if (cause instanceof HTTPValidationErrorException) {
        HTTPValidationErrorException hTTPValidationErrorException = (HTTPValidationErrorException) cause;
        hTTPValidationErrorException.printStackTrace();
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
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/java/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](http://localhost:3000/llms-pages/java/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/java/models/exceptions/error-body.md) |



