# Get Paypal Disputes

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0ZSUyRnBheXBhbCUyRmdldF9wYXlwYWxfZGlzcHV0ZXM

List Disputes. Local console route GET /api/v1/paypal/disputes on synthetic data; advisory only.

```csharp
GetPaypalDisputesAsync()
```


# Authentication

This endpoint requires [DemoSession](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/getting-started/how-to-get-started/authorization.md)


# Response Type

**200**: Successful Response

[`Task<Models.DisputeListResponse>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/dispute-list-response.md)


# Example Usage

```csharp
try
{
    DisputeListResponse result = await paypalController.GetPaypalDisputesAsync();
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
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/exceptions/error-body.md) |



