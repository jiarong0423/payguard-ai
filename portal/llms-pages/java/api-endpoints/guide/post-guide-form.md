# Post Guide Form

Source: http://localhost:3000/#/java/x-redirect/JTI0ZSUyRmd1aWRlJTJGcG9zdF9ndWlkZV9mb3Jt

Guide Form. Local console route POST /api/v1/guide/form on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```java
CompletableFuture<GuideStateResponse> postGuideFormAsync(
    final GuideFormRequest body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`GuideFormRequest`](http://localhost:3000/llms-pages/java/models/structures/guide-form-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`GuideStateResponse`](http://localhost:3000/llms-pages/java/models/structures/guide-state-response.md)


# Example Usage

```java
GuideFormRequest body = new GuideFormRequest.Builder()
    .confirmReview(false)
    .build();

guideController.postGuideFormAsync(body).thenAccept(result -> {
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



