# Get Ai Usage

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0ZSUyRmFpJTJGZ2V0X2FpX3VzYWdl

(optimise r24) This session's AI calls: stage, model, tokens, latency, estimated cost. No prompt or reply
text is ever stored; the hosted demo makes no model call and answers an empty list.

:information_source: **Note** This endpoint does not require authentication.

```csharp
GetAiUsageAsync()
```


# Response Type

**200**: Successful Response

[`Task<Models.AiUsageResponse>`](http://localhost:3000/llms-pages/net-standard-library/models/structures/ai-usage-response.md)


# Example Usage

```csharp
try
{
    AiUsageResponse result = await aiController.GetAiUsageAsync();
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



