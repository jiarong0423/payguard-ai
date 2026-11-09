# Get Demo State

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0ZSUyRmRlbW8lMkZnZXRfZGVtb19zdGF0ZQ

State. Local console route GET /api/v1/demo/state on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```csharp
GetDemoStateAsync()
```


# Response Type

**200**: Successful Response

[`Task<Models.StateResponse>`](http://localhost:3000/llms-pages/net-standard-library/models/structures/state-response.md)


# Example Usage

```csharp
try
{
    StateResponse result = await demoController.GetDemoStateAsync();
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



