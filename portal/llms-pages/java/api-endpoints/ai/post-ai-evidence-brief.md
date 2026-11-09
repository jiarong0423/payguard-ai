# Post Ai Evidence Brief

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0ZSUyRmFpJTJGcG9zdF9haV9ldmlkZW5jZV9icmllZg

Evidence Brief. Local console route POST /api/v1/ai/evidence-brief on synthetic data; advisory only. The hosted demo answers 503 hosted_demo_disabled here: it makes no provider calls.

:information_source: **Note** This endpoint does not require authentication.

```java
CompletableFuture<AiBriefResponse> postAiEvidenceBriefAsync(
    final AiBriefHttpRequest body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`AiBriefHttpRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/ai-brief-http-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`AiBriefResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/ai-brief-response.md)


# Example Usage

```java
AiBriefHttpRequest body = new AiBriefHttpRequest.Builder(
    StageEnum.VELOCITY_GUARD
)
.build();

aiController.postAiEvidenceBriefAsync(body).thenAccept(result -> {
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



