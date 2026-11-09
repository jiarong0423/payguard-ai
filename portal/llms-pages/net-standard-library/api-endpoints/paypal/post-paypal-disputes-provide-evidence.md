# Post Paypal Disputes Provide Evidence

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0ZSUyRnBheXBhbCUyRnBvc3RfcGF5cGFsX2Rpc3B1dGVzX3Byb3ZpZGVfZXZpZGVuY2U

Provide Evidence. Local console route POST /api/v1/paypal/disputes/provide-evidence on synthetic data; advisory only. The hosted demo answers 503 hosted_demo_disabled here: it makes no provider calls.

:information_source: **Note** This endpoint does not require authentication.

```csharp
PostPaypalDisputesProvideEvidenceAsync(
    Models.ProvideEvidenceRequest body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`ProvideEvidenceRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/provide-evidence-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`Task<Models.ProvideEvidenceResponse>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/provide-evidence-response.md)


# Example Usage

```csharp
ProvideEvidenceRequest body = new ProvideEvidenceRequest
{
    CaseRef = "case_ref0",
    DisputeId = "dispute_id8",
    Submit = false,
};

try
{
    ProvideEvidenceResponse result = await paypalController.PostPaypalDisputesProvideEvidenceAsync(body);
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



