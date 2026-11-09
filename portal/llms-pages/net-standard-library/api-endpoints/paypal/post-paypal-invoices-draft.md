# Post Paypal Invoices Draft

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0ZSUyRnBheXBhbCUyRnBvc3RfcGF5cGFsX2ludm9pY2VzX2RyYWZ0

Invoice Draft. Local console route POST /api/v1/paypal/invoices/draft on synthetic data; advisory only. The hosted demo answers 503 hosted_demo_disabled here: it makes no provider calls.

:information_source: **Note** This endpoint does not require authentication.

```csharp
PostPaypalInvoicesDraftAsync(
    Models.InvoiceDraftRequest body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`InvoiceDraftRequest`](http://localhost:3000/llms-pages/net-standard-library/models/structures/invoice-draft-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`Task<Models.InvoiceDraftResponse>`](http://localhost:3000/llms-pages/net-standard-library/models/structures/invoice-draft-response.md)


# Example Usage

```csharp
InvoiceDraftRequest body = new InvoiceDraftRequest
{
    Amount = "amount8",
    Currency = CurrencyEnum.USD,
    Description = "description4",
    PayloadDigest = "payload_digest4",
    ReviewToken = "review_token4",
};

try
{
    InvoiceDraftResponse result = await paypalController.PostPaypalInvoicesDraftAsync(body);
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



