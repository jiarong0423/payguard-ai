# Post Paypal Disputes Add Tracking

Source: http://localhost:3000/#/net-standard-library/x-redirect/JTI0ZSUyRnBheXBhbCUyRnBvc3RfcGF5cGFsX2Rpc3B1dGVzX2FkZF90cmFja2luZw

Add Tracking. Local console route POST /api/v1/paypal/disputes/add-tracking on synthetic data; advisory only. The hosted demo answers 503 hosted_demo_disabled here: it makes no provider calls.

:information_source: **Note** This endpoint does not require authentication.

```csharp
PostPaypalDisputesAddTrackingAsync(
    Models.AddTrackingRequest body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`AddTrackingRequest`](http://localhost:3000/llms-pages/net-standard-library/models/structures/add-tracking-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`Task<Models.AddTrackingResponse>`](http://localhost:3000/llms-pages/net-standard-library/models/structures/add-tracking-response.md)


# Example Usage

```csharp
AddTrackingRequest body = new AddTrackingRequest
{
    CaseRef = "case_ref0",
    DisputeId = "dispute_id8",
    Submit = false,
};

try
{
    AddTrackingResponse result = await paypalController.PostPaypalDisputesAddTrackingAsync(body);
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



