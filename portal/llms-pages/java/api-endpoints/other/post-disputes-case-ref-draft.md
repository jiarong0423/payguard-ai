# Post Disputes Case Ref Draft

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0ZSUyRm90aGVyJTJGcG9zdF9kaXNwdXRlc19jYXNlX3JlZl9kcmFmdA

Draft. Local console route POST /api/v1/disputes/{case_ref}/draft on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```java
CompletableFuture<DisputeDraftResponse> postDisputesCaseRefDraftAsync(
    final String caseRef,
    final Object body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `caseRef` | `String` | Template, Required | Case ref. |
| `body` | `Object` | Body, Required | - |


# Response Type

**200**: Successful Response

[`DisputeDraftResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/dispute-draft-response.md)


# Example Usage

```java
String caseRef = "case_ref4";
Object body = ApiHelper.deserialize("{\"key1\":\"val1\",\"key2\":\"val2\"}");

otherController.postDisputesCaseRefDraftAsync(caseRef, body).thenAccept(result -> {
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
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/exceptions/error-body.md) |



