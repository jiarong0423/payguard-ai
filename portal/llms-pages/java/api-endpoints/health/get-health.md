# Get Health

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0ZSUyRmhlYWx0aCUyRmdldF9oZWFsdGg

Health. Local console route GET /api/v1/health on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```java
CompletableFuture<HealthResponse> getHealthAsync()
```


# Response Type

**200**: Successful Response

[`HealthResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/health-response.md)


# Example Usage

```java
healthController.getHealthAsync().thenAccept(result -> {
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


# Example Response *(as JSON)*

```json
{
  "mode": "demo",
  "source": "synthetic",
  "status": "ok",
  "version": "0.0.0-example"
}
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/exceptions/error-body.md) |



