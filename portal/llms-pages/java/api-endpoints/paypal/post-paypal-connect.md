# Post Paypal Connect

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0ZSUyRnBheXBhbCUyRnBvc3RfcGF5cGFsX2Nvbm5lY3Q

Connect. Local console route POST /api/v1/paypal/connect on synthetic data; advisory only. The hosted demo answers 503 hosted_demo_disabled here: it makes no provider calls.

:information_source: **Note** This endpoint does not require authentication.

```java
CompletableFuture<PaypalStatusResponse> postPaypalConnectAsync(
    final Object body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | `Object` | Body, Required | - |


# Response Type

**200**: Successful Response

[`PaypalStatusResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/paypal-status-response.md)


# Example Usage

```java
Object body = ApiHelper.deserialize("{\"key1\":\"val1\",\"key2\":\"val2\"}");

paypalController.postPaypalConnectAsync(body).thenAccept(result -> {
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



