# Post Aup Acknowledge

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0ZSUyRmF1cCUyRnBvc3RfYXVwX2Fja25vd2xlZGdl

Acknowledge Aup. Local console route POST /api/v1/aup/acknowledge on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```csharp
PostAupAcknowledgeAsync(
    Models.AupAcknowledgeRequest body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`AupAcknowledgeRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/aup-acknowledge-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`Task<Models.AupAcknowledgeResponse>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/aup-acknowledge-response.md)


# Example Usage

```csharp
AupAcknowledgeRequest body = new AupAcknowledgeRequest
{
    Choice = ChoiceEnum.CANCEL,
    DescriptionDigest = "description_digest4",
    EvaluationId = "evaluation_id0",
};

try
{
    AupAcknowledgeResponse result = await aupController.PostAupAcknowledgeAsync(body);
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



