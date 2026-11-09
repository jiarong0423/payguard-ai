# Post Advisory Evaluate

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0ZSUyRm90aGVyJTJGcG9zdF9hZHZpc29yeV9ldmFsdWF0ZQ

Advisory Evaluate. Local console route POST /api/v1/advisory/evaluate on synthetic data; advisory only.

```csharp
PostAdvisoryEvaluateAsync(
    Models.AdvisoryRequest body)
```


# Authentication

This endpoint requires [DemoCsrf](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/getting-started/how-to-get-started/authorization.md) **AND** [DemoSession](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/getting-started/how-to-get-started/authorization.md)


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`AdvisoryRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/advisory-request.md) | Body, Required | JSON body for: Advisory Evaluate. |


# Response Type

**200**: Successful Response

[`Task<Models.AdvisoryEvaluationResponse>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/advisory-evaluation-response.md)


# Example Usage

```csharp
AdvisoryRequest body = new AdvisoryRequest
{
    AsOf = "examplexxxxxxxxxxxxx",
    CandidateJson = "example",
    Jurisdiction = "US",
    ObservationMaxAgeDays = 0,
    Theme = ThemeEnum.SourceCompliance,
};

try
{
    AdvisoryEvaluationResponse result = await otherController.PostAdvisoryEvaluateAsync(body);
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
| 403 | Origin missing or not allowed, or the CSRF token is wrong (origin_required, origin_rejected, csrf_rejected). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/exceptions/error-body.md) |
| 422 | The request does not match the accepted contract (schema_invalid). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/exceptions/error-body.md) |



