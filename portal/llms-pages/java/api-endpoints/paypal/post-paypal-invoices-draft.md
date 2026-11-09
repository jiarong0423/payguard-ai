# Post Paypal Invoices Draft

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0ZSUyRnBheXBhbCUyRnBvc3RfcGF5cGFsX2ludm9pY2VzX2RyYWZ0

Invoice Draft. Local console route POST /api/v1/paypal/invoices/draft on synthetic data; advisory only. The hosted demo answers 503 hosted_demo_disabled here: it makes no provider calls.

:information_source: **Note** This endpoint does not require authentication.

```java
CompletableFuture<InvoiceDraftResponse> postPaypalInvoicesDraftAsync(
    final InvoiceDraftRequest body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`InvoiceDraftRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/invoice-draft-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`InvoiceDraftResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/invoice-draft-response.md)


# Example Usage

```java
InvoiceDraftRequest body = new InvoiceDraftRequest.Builder(
    "amount8",
    CurrencyEnum.USD,
    "description4",
    "payload_digest4",
    "review_token4"
)
.build();

paypalController.postPaypalInvoicesDraftAsync(body).thenAccept(result -> {
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



