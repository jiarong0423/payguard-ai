# Post Guide Turn

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0ZSUyRmd1aWRlJTJGcG9zdF9ndWlkZV90dXJu

Guide Turn. Local console route POST /api/v1/guide/turn on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```csharp
PostGuideTurnAsync(
    Models.GuideTurnRequest body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`GuideTurnRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/guide-turn-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`Task<Models.GuideStateResponse>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/guide-state-response.md)


# Example Usage

```csharp
GuideTurnRequest body = new GuideTurnRequest
{
    Text = "text4",
};

try
{
    GuideStateResponse result = await guideController.PostGuideTurnAsync(body);
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



