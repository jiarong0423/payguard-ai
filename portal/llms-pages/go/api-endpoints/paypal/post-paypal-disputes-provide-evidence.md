# Post Paypal Disputes Provide Evidence

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0ZSUyRnBheXBhbCUyRnBvc3RfcGF5cGFsX2Rpc3B1dGVzX3Byb3ZpZGVfZXZpZGVuY2U

Provide Evidence. Local console route POST /api/v1/paypal/disputes/provide-evidence on synthetic data; advisory only. The hosted demo answers 503 hosted_demo_disabled here: it makes no provider calls.

:information_source: **Note** This endpoint does not require authentication.

```go
PostPaypalDisputesProvideEvidence(
    ctx context.Context,
    body models.ProvideEvidenceRequest) (
    models.ApiResponse[models.ProvideEvidenceResponse],
    error)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`models.ProvideEvidenceRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/provide-evidence-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

This method returns an [`ApiResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/sdk-infrastructure/utilities/apiresponse.md) instance. The `Data` property of this instance returns the response data which is of type [models.ProvideEvidenceResponse](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/provide-evidence-response.md).


# Example Usage

```go
ctx := context.Background()

body := models.ProvideEvidenceRequest{
    CaseRef:      "case_ref0",
    DisputeId:    "dispute_id8",
    Submit:       models.ToPointer(false),
}

apiResponse, err := paypalController.PostPaypalDisputesProvideEvidence(ctx, body)
if err != nil {
    switch typedErr := err.(type) {
        case *errors.ErrorBody:
            log.Fatalln("ErrorBodyException: ", typedErr)
        case *errors.HTTPValidationError:
            log.Fatalln("HTTPValidationErrorException: ", typedErr)
        default:
            log.Fatalln(err)
    }
} else {
    // Printing the result and response
    fmt.Println(apiResponse.Data)
    fmt.Println(apiResponse.Response.StatusCode)
}
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/exceptions/error-body.md) |



