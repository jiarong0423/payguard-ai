# Post Aup Product Reference

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0ZSUyRmF1cCUyRnBvc3RfYXVwX3Byb2R1Y3RfcmVmZXJlbmNl

Aup Product Reference. Local console route POST /api/v1/aup/product-reference on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```csharp
PostAupProductReferenceAsync(
    Models.ProductReferenceRequest body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`ProductReferenceRequest`](http://localhost:3000/llms-pages/net-standard-library/models/structures/product-reference-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`Task<Models.ProductReferenceResponse>`](http://localhost:3000/llms-pages/net-standard-library/models/structures/product-reference-response.md)


# Example Usage

```csharp
ProductReferenceRequest body = new ProductReferenceRequest
{
    Description = "description4",
    EvaluationId = "evaluation_id0",
};

try
{
    ProductReferenceResponse result = await aupController.PostAupProductReferenceAsync(body);
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



