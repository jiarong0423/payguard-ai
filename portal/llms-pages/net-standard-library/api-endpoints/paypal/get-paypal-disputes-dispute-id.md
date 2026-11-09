# Get Paypal Disputes Dispute Id

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0ZSUyRnBheXBhbCUyRmdldF9wYXlwYWxfZGlzcHV0ZXNfZGlzcHV0ZV9pZA

Get Dispute. Local console route GET /api/v1/paypal/disputes/{dispute_id} on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```csharp
GetPaypalDisputesDisputeIdAsync(
    string disputeId)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `disputeId` | `string` | Template, Required | Dispute id. |


# Response Type

**200**: Successful Response

[`Task<Models.DisputeDetailResponse>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/dispute-detail-response.md)


# Example Usage

```csharp
string disputeId = "dispute_id2";
try
{
    DisputeDetailResponse result = await paypalController.GetPaypalDisputesDisputeIdAsync(disputeId);
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



