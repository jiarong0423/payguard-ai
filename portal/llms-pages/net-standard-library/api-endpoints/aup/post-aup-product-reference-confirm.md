# Post Aup Product Reference Confirm

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0ZSUyRmF1cCUyRnBvc3RfYXVwX3Byb2R1Y3RfcmVmZXJlbmNlX2NvbmZpcm0

Aup Product Confirm. Local console route POST /api/v1/aup/product-reference/confirm on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```csharp
PostAupProductReferenceConfirmAsync(
    Models.ProductConfirmRequest body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`ProductConfirmRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/product-confirm-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`Task<Models.ProductConfirmResponse>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/product-confirm-response.md)


# Example Usage

```csharp
ProductConfirmRequest body = new ProductConfirmRequest
{
    Description = "description4",
    EvaluationId = "evaluation_id0",
    ProductId = ProductConfirmRequestProductId.FromString("String3"),
};

try
{
    ProductConfirmResponse result = await aupController.PostAupProductReferenceConfirmAsync(body);
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
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/exceptions/error-body.md) |



