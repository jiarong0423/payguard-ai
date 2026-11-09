# Post Disputes Case Ref Draft

Source: https://jiarong0423.github.io/payguard-ai/portal/#/net-standard-library/x-redirect/JTI0ZSUyRm90aGVyJTJGcG9zdF9kaXNwdXRlc19jYXNlX3JlZl9kcmFmdA

Draft. Local console route POST /api/v1/disputes/{case_ref}/draft on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```csharp
PostDisputesCaseRefDraftAsync(
    string caseRef,
    object body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `caseRef` | `string` | Template, Required | Case ref. |
| `body` | `object` | Body, Required | - |


# Response Type

**200**: Successful Response

[`Task<Models.DisputeDraftResponse>`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/net-standard-library/models/structures/dispute-draft-response.md)


# Example Usage

```csharp
string caseRef = "case_ref4";
object body = ApiHelper.JsonDeserialize<object>("{\"key1\":\"val1\",\"key2\":\"val2\"}");
try
{
    DisputeDraftResponse result = await otherController.PostDisputesCaseRefDraftAsync(
        caseRef,
        body
    );
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



