# Get Guide State

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0ZSUyRmd1aWRlJTJGZ2V0X2d1aWRlX3N0YXRl

Guide State. Local console route GET /api/v1/guide/state on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```java
CompletableFuture<GuideStateResponse> getGuideStateAsync(
    final GetGuideStateScenario scenario)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `scenario` | [`GetGuideStateScenario`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/oneof-anyof-definitions/get-guide-state-scenario.md) | Query, Optional | This is a container for any-of cases. |


# Response Type

**200**: Successful Response

[`GuideStateResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/guide-state-response.md)


# Example Usage

```java
guideController.getGuideStateAsync(null).thenAccept(result -> {
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



