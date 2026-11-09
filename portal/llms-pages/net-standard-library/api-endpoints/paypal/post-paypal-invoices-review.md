# Post Paypal Invoices Review

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0ZSUyRnBheXBhbCUyRnBvc3RfcGF5cGFsX2ludm9pY2VzX3Jldmlldw

Invoice Review. Local console route POST /api/v1/paypal/invoices/review on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```csharp
PostPaypalInvoicesReviewAsync(
    Models.InvoiceReviewRequest body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`InvoiceReviewRequest`](http://localhost:3000/llms-pages/net-standard-library/models/structures/invoice-review-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`Task<Models.InvoiceReviewResponse>`](http://localhost:3000/llms-pages/net-standard-library/models/structures/invoice-review-response.md)


# Example Usage

```csharp
InvoiceReviewRequest body = new InvoiceReviewRequest
{
    Amount = "amount8",
    ConfirmSandboxDraft = false,
    Currency = CurrencyEnum.USD,
    Description = "description4",
};

try
{
    InvoiceReviewResponse result = await paypalController.PostPaypalInvoicesReviewAsync(body);
}
catch (ApiException e)
{
    Console.WriteLine(e.Message);
    if (e is ErrorBodyException)
    {
       // TODO: Handle ErrorBodyException exception here
    }
    if (e is HTTPValidationErrorException)
    {
       // TODO: Handle HTTPValidationErrorException exception here
    }
}
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/net-standard-library/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](http://localhost:3000/llms-pages/net-standard-library/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/net-standard-library/models/exceptions/error-body.md) |



