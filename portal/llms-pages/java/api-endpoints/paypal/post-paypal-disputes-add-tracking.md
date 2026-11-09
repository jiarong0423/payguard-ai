# Post Paypal Disputes Add Tracking

Source: https://jiarong0423.github.io/payguard-ai/portal/#/java/x-redirect/JTI0ZSUyRnBheXBhbCUyRnBvc3RfcGF5cGFsX2Rpc3B1dGVzX2FkZF90cmFja2luZw

Add Tracking. Local console route POST /api/v1/paypal/disputes/add-tracking on synthetic data; advisory only. The hosted demo answers 503 hosted_demo_disabled here: it makes no provider calls.

:information_source: **Note** This endpoint does not require authentication.

```java
CompletableFuture<AddTrackingResponse> postPaypalDisputesAddTrackingAsync(
    final AddTrackingRequest body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`AddTrackingRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/add-tracking-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`AddTrackingResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/java/models/structures/add-tracking-response.md)


# Example Usage

```java
AddTrackingRequest body = new AddTrackingRequest.Builder(
    "case_ref0",
    "dispute_id8"
)
.submit(false)
.build();

paypalController.postPaypalDisputesAddTrackingAsync(body).thenAccept(result -> {
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



