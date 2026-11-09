# Post Cases Route

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0ZSUyRm90aGVyJTJGcG9zdF9jYXNlc19yb3V0ZQ

Case Route. Local console route POST /api/v1/cases/route on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```csharp
PostCasesRouteAsync(
    Models.CaseRouteRequest body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`CaseRouteRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/case-route-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`Task<Models.CaseRouteResponse>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/case-route-response.md)


# Example Usage

```csharp
CaseRouteRequest body = new CaseRouteRequest
{
    Text = "text4",
};

try
{
    CaseRouteResponse result = await otherController.PostCasesRouteAsync(body);
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



