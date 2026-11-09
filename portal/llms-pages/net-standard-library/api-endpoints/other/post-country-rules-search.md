# Post Country Rules Search

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0ZSUyRm90aGVyJTJGcG9zdF9jb3VudHJ5X3J1bGVzX3NlYXJjaA

Country Rules Search. Local console route POST /api/v1/country-rules/search on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```csharp
PostCountryRulesSearchAsync(
    Models.CountryRulesSearchRequest body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`CountryRulesSearchRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/country-rules-search-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

`Task<object>`


# Example Usage

```csharp
CountryRulesSearchRequest body = new CountryRulesSearchRequest
{
    Query = "query6",
    Limit = 5,
};

try
{
    object result = await otherController.PostCountryRulesSearchAsync(body);
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



