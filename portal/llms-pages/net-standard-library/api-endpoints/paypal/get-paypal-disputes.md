# Get Paypal Disputes

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0ZSUyRnBheXBhbCUyRmdldF9wYXlwYWxfZGlzcHV0ZXM

List Disputes. Local console route GET /api/v1/paypal/disputes on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```csharp
GetPaypalDisputesAsync()
```


# Response Type

**200**: Successful Response

[`Task<Models.DisputeListResponse>`](http://localhost:3000/llms-pages/net-standard-library/models/structures/dispute-list-response.md)


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
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/net-standard-library/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/net-standard-library/models/exceptions/error-body.md) |



