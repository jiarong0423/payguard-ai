# Post Ai Evidence Brief

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0ZSUyRmFpJTJGcG9zdF9haV9ldmlkZW5jZV9icmllZg

Evidence Brief. Local console route POST /api/v1/ai/evidence-brief on synthetic data; advisory only. The hosted demo answers 503 hosted_demo_disabled here: it makes no provider calls.

:information_source: **Note** This endpoint does not require authentication.

```csharp
PostAiEvidenceBriefAsync(
    Models.AiBriefHttpRequest body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`AiBriefHttpRequest`](http://localhost:3000/llms-pages/net-standard-library/models/structures/ai-brief-http-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`Task<Models.AiBriefResponse>`](http://localhost:3000/llms-pages/net-standard-library/models/structures/ai-brief-response.md)


# Example Usage

```csharp
AiBriefHttpRequest body = new AiBriefHttpRequest
{
    Stage = StageEnum.VelocityGuard,
};

try
{
    AiBriefResponse result = await aiController.PostAiEvidenceBriefAsync(body);
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



