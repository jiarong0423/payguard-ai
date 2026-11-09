# Post Advisory Evaluate

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0ZSUyRm90aGVyJTJGcG9zdF9hZHZpc29yeV9ldmFsdWF0ZQ

Advisory Evaluate. Local console route POST /api/v1/advisory/evaluate on synthetic data; advisory only.

```go
PostAdvisoryEvaluate(
    ctx context.Context,
    body models.AdvisoryRequest) (
    models.ApiResponse[models.AdvisoryEvaluationResponse],
    error)
```


# Authentication

This endpoint requires [DemoCsrf](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/getting-started/how-to-get-started/authorization.md) **AND** [DemoSession](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/getting-started/how-to-get-started/authorization.md)


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`models.AdvisoryRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/advisory-request.md) | Body, Required | JSON body for: Advisory Evaluate. |


# Response Type

**200**: Successful Response

This method returns an [`ApiResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/sdk-infrastructure/utilities/apiresponse.md) instance. The `Data` property of this instance returns the response data which is of type [models.AdvisoryEvaluationResponse](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/advisory-evaluation-response.md).


# Example Usage

```go
ctx := context.Background()

body := models.AdvisoryRequest{
    AsOf:                  "examplexxxxxxxxxxxxx",
    CandidateJson:         "example",
    Jurisdiction:          "US",
    ObservationMaxAgeDays: 0,
    Theme:                 models.ThemeEnum_SOURCECOMPLIANCE,
}

apiResponse, err := otherController.PostAdvisoryEvaluate(ctx, body)
if err != nil {
    switch typedErr := err.(type) {
        case *errors.ErrorBody:
            log.Fatalln("ErrorBodyException: ", typedErr)
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
| 403 | Origin missing or not allowed, or the CSRF token is wrong (origin_required, origin_rejected, csrf_rejected). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/exceptions/error-body.md) |
| 422 | The request does not match the accepted contract (schema_invalid). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/exceptions/error-body.md) |



