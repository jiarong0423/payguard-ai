# Post Aup Review

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0ZSUyRmF1cCUyRnBvc3RfYXVwX3Jldmlldw

Aup. Local console route POST /api/v1/aup/review on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```csharp
PostAupReviewAsync(
    Models.AupRequest body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`AupRequest`](http://localhost:3000/llms-pages/net-standard-library/models/structures/aup-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`Task<Models.AupResponse>`](http://localhost:3000/llms-pages/net-standard-library/models/structures/aup-response.md)


# Example Usage

```csharp
AupRequest body = new AupRequest
{
    Description = "description4",
};

try
{
    AupResponse result = await aupController.PostAupReviewAsync(body);
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



