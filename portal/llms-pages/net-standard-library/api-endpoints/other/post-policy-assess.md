# Post Policy Assess

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0ZSUyRm90aGVyJTJGcG9zdF9wb2xpY3lfYXNzZXNz

Policy Assess. Local console route POST /api/v1/policy/assess on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```csharp
PostPolicyAssessAsync(
    Models.PolicyRequest body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`PolicyRequest`](http://localhost:3000/llms-pages/net-standard-library/models/structures/policy-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`Task<Models.PolicyAssessmentResponse>`](http://localhost:3000/llms-pages/net-standard-library/models/structures/policy-assessment-response.md)


# Example Usage

```csharp
PolicyRequest body = new PolicyRequest
{
    AsOf = "as_of2",
    Jurisdiction = "US",
    ObservationMaxAgeDays = 102,
    Theme = ThemeEnum.DisputeMediation,
};

try
{
    PolicyAssessmentResponse result = await otherController.PostPolicyAssessAsync(body);
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



