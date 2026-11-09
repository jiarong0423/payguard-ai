# Get Guide State

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0ZSUyRmd1aWRlJTJGZ2V0X2d1aWRlX3N0YXRl

Guide State. Local console route GET /api/v1/guide/state on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```csharp
GetGuideStateAsync(
    GetGuideStateScenario scenario = null)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `scenario` | [`GetGuideStateScenario`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/oneof-anyof-definitions/get-guide-state-scenario.md) | Query, Optional | This is a container for any-of cases. |


# Response Type

**200**: Successful Response

[`Task<Models.GuideStateResponse>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/guide-state-response.md)


# Example Usage

```csharp
try
{
    GuideStateResponse result = await guideController.GetGuideStateAsync();
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



