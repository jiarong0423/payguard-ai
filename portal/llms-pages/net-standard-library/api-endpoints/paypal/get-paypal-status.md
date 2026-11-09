# Get Paypal Status

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0ZSUyRnBheXBhbCUyRmdldF9wYXlwYWxfc3RhdHVz

Paypal Status. Local console route GET /api/v1/paypal/status on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```csharp
GetPaypalStatusAsync()
```


# Response Type

**200**: Successful Response

[`Task<Models.PaypalStatusResponse>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/paypal-status-response.md)


# Example Usage

```csharp
try
{
    PaypalStatusResponse result = await paypalController.GetPaypalStatusAsync();
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



