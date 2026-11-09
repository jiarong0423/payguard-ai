# Post Paypal Invoices Draft

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0ZSUyRnBheXBhbCUyRnBvc3RfcGF5cGFsX2ludm9pY2VzX2RyYWZ0

Invoice Draft. Local console route POST /api/v1/paypal/invoices/draft on synthetic data; advisory only. The hosted demo answers 503 hosted_demo_disabled here: it makes no provider calls.

:information_source: **Note** This endpoint does not require authentication.

```go
PostPaypalInvoicesDraft(
    ctx context.Context,
    body models.InvoiceDraftRequest) (
    models.ApiResponse[models.InvoiceDraftResponse],
    error)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`models.InvoiceDraftRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/invoice-draft-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

This method returns an [`ApiResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/sdk-infrastructure/utilities/apiresponse.md) instance. The `Data` property of this instance returns the response data which is of type [models.InvoiceDraftResponse](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/invoice-draft-response.md).


# Example Usage

```go
ctx := context.Background()

body := models.InvoiceDraftRequest{
    Amount:        "amount8",
    Currency:      models.CurrencyEnum_USD,
    Description:   "description4",
    PayloadDigest: "payload_digest4",
    ReviewToken:   "review_token4",
}

apiResponse, err := paypalController.PostPaypalInvoicesDraft(ctx, body)
if err != nil {
    switch typedErr := err.(type) {
        case *errors.ErrorBody:
            log.Fatalln("ErrorBodyException: ", typedErr)
        case *errors.HTTPValidationError:
            log.Fatalln("HTTPValidationErrorException: ", typedErr)
        default:
            log.Fatalln(err)
    }
} else {
    // Printing the result and response
    fmt.Println(apiResponse.Data)
    fmt.Println(apiResponse.Response.StatusCode)
}
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/exceptions/error-body.md) |



