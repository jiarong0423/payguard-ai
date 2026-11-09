# Get Studio Agent Status

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0ZSUyRnN0dWRpbyUyRmdldF9zdHVkaW9fYWdlbnRfc3RhdHVz

Studio Agent Status. Local console route GET /api/v1/studio/agent-status on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```java
CompletableFuture<Object> getStudioAgentStatusAsync()
```


# Response Type

**200**: Successful Response

`Object`


# Example Usage

```java
studioController.getStudioAgentStatusAsync().thenAccept(result -> {
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
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/exceptions/error-body.md) |



