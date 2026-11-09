# Post Policy Assess

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0ZSUyRm90aGVyJTJGcG9zdF9wb2xpY3lfYXNzZXNz

Policy Assess. Local console route POST /api/v1/policy/assess on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```go
PostPolicyAssess(
    ctx context.Context,
    body models.PolicyRequest) (
    models.ApiResponse[models.PolicyAssessmentResponse],
    error)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`models.PolicyRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/policy-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

This method returns an [`ApiResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/sdk-infrastructure/utilities/apiresponse.md) instance. The `Data` property of this instance returns the response data which is of type [models.PolicyAssessmentResponse](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/policy-assessment-response.md).


# Example Usage

```go
ctx := context.Background()

body := models.PolicyRequest{
    AsOf:                  "as_of2",
    Jurisdiction:          "US",
    ObservationMaxAgeDays: 102,
    Theme:                 models.ThemeEnum_DISPUTEMEDIATION,
}

apiResponse, err := otherController.PostPolicyAssess(ctx, body)
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



