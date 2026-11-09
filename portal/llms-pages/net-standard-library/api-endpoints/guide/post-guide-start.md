# Post Guide Start

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0ZSUyRmd1aWRlJTJGcG9zdF9ndWlkZV9zdGFydA

Guide Start. Local console route POST /api/v1/guide/start on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```csharp
PostGuideStartAsync(
    Models.GuideStartRequest body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`GuideStartRequest`](http://localhost:3000/llms-pages/net-standard-library/models/structures/guide-start-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`Task<Models.GuideStateResponse>`](http://localhost:3000/llms-pages/net-standard-library/models/structures/guide-state-response.md)


# Example Usage

```csharp
GuideStartRequest body = new GuideStartRequest
{
    Scenario = Scenario2Enum.Velocity,
};

try
{
    GuideStateResponse result = await guideController.PostGuideStartAsync(body);
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
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/net-standard-library/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](http://localhost:3000/llms-pages/net-standard-library/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/net-standard-library/models/exceptions/error-body.md) |



