# Post Demo Inject

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0ZSUyRmRlbW8lMkZwb3N0X2RlbW9faW5qZWN0

Inject. Local console route POST /api/v1/demo/inject on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```csharp
PostDemoInjectAsync(
    Models.InjectRequest body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`InjectRequest`](http://localhost:3000/llms-pages/net-standard-library/models/structures/inject-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`Task<Models.StateResponse>`](http://localhost:3000/llms-pages/net-standard-library/models/structures/state-response.md)


# Example Usage

```csharp
InjectRequest body = new InjectRequest
{
    Scenario = Scenario5Enum.Dispute,
};

try
{
    StateResponse result = await demoController.PostDemoInjectAsync(body);
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



