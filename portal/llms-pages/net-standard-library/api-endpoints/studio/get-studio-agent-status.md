# Get Studio Agent Status

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0ZSUyRnN0dWRpbyUyRmdldF9zdHVkaW9fYWdlbnRfc3RhdHVz

Studio Agent Status. Local console route GET /api/v1/studio/agent-status on synthetic data; advisory only.

```csharp
GetStudioAgentStatusAsync()
```


# Authentication

This endpoint requires [DemoSession](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/getting-started/how-to-get-started/authorization.md)


# Response Type

**200**: Successful Response

`Task<object>`


# Example Usage

```csharp
try
{
    object result = await studioController.GetStudioAgentStatusAsync();
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



