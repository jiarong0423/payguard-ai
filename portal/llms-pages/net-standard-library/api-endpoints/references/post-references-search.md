# Post References Search

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0ZSUyRnJlZmVyZW5jZXMlMkZwb3N0X3JlZmVyZW5jZXNfc2VhcmNo

References. Local console route POST /api/v1/references/search on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```csharp
PostReferencesSearchAsync(
    Models.ReferenceRequest body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`ReferenceRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/reference-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`Task<Models.ReferenceResponse>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/reference-response.md)


# Example Usage

```csharp
ReferenceRequest body = new ReferenceRequest
{
    Jurisdiction = "US",
    Query = "query6",
    Theme = ThemeEnum.DisputeMediation,
    CaseStage = CaseStage2Enum.Any,
    Limit = 3,
    RequireKnownSourceDate = false,
};

try
{
    ReferenceResponse result = await referencesController.PostReferencesSearchAsync(body);
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



