# Post Aup Acknowledge

Source: http://localhost:3000/#/java/x-redirect/JTI0ZSUyRmF1cCUyRnBvc3RfYXVwX2Fja25vd2xlZGdl

Acknowledge Aup. Local console route POST /api/v1/aup/acknowledge on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```java
CompletableFuture<AupAcknowledgeResponse> postAupAcknowledgeAsync(
    final AupAcknowledgeRequest body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`AupAcknowledgeRequest`](http://localhost:3000/llms-pages/java/models/structures/aup-acknowledge-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`AupAcknowledgeResponse`](http://localhost:3000/llms-pages/java/models/structures/aup-acknowledge-response.md)


# Example Usage

```java
AupAcknowledgeRequest body = new AupAcknowledgeRequest.Builder(
    ChoiceEnum.CANCEL,
    "description_digest4",
    "evaluation_id0"
)
.build();

aupController.postAupAcknowledgeAsync(body).thenAccept(result -> {
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



