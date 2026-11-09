# Get Health

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0ZSUyRmhlYWx0aCUyRmdldF9oZWFsdGg

Health. Local console route GET /api/v1/health on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```csharp
GetHealthAsync()
```


# Response Type

**200**: Successful Response

[`Task<Models.HealthResponse>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/health-response.md)


# Example Usage

```csharp
try
{
    HealthResponse result = await healthController.GetHealthAsync();
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



