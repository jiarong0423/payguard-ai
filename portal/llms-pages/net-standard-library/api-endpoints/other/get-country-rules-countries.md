# Get Country Rules Countries

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0ZSUyRm90aGVyJTJGZ2V0X2NvdW50cnlfcnVsZXNfY291bnRyaWVz

Country Rules Countries. Local console route GET /api/v1/country-rules/countries on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```csharp
GetCountryRulesCountriesAsync()
```


# Response Type

**200**: Successful Response

`Task<object>`


# Example Usage

```csharp
try
{
    object result = await otherController.GetCountryRulesCountriesAsync();
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



