# Post Aup Product Reference

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0ZSUyRmF1cCUyRnBvc3RfYXVwX3Byb2R1Y3RfcmVmZXJlbmNl

Aup Product Reference. Local console route POST /api/v1/aup/product-reference on synthetic data; advisory only.

```csharp
PostAupProductReferenceAsync(
    Models.ProductReferenceRequest body)
```


# Authentication

This endpoint requires [DemoCsrf](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/getting-started/how-to-get-started/authorization.md) **AND** [DemoSession](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/getting-started/how-to-get-started/authorization.md)


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`ProductReferenceRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/product-reference-request.md) | Body, Required | JSON body for: Aup Product Reference. |


# Response Type

**200**: Successful Response

[`Task<Models.ProductReferenceResponse>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/product-reference-response.md)


# Example Usage

```csharp
ProductReferenceRequest body = new ProductReferenceRequest
{
    Description = "example",
    EvaluationId = "examplexxxxxxxxxxxxxxxxxxxxxxxxx",
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
}
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/exceptions/error-body.md) |
| 403 | Origin missing or not allowed, or the CSRF token is wrong (origin_required, origin_rejected, csrf_rejected). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/exceptions/error-body.md) |
| 422 | The request does not match the accepted contract (schema_invalid). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/exceptions/error-body.md) |



