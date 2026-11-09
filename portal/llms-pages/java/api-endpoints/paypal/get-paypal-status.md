# Get Paypal Status

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0ZSUyRnBheXBhbCUyRmdldF9wYXlwYWxfc3RhdHVz

Paypal Status. Local console route GET /api/v1/paypal/status on synthetic data; advisory only.

```java
CompletableFuture<PaypalStatusResponse> getPaypalStatusAsync()
```


# Authentication

This endpoint requires [DemoSession](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/getting-started/how-to-get-started/authorization.md)


# Response Type

**200**: Successful Response

[`PaypalStatusResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/paypal-status-response.md)


# Example Usage

```java
paypalController.getPaypalStatusAsync().thenAccept(result -> {
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



