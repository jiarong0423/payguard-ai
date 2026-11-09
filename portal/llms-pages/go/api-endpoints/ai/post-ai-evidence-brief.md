# Post Ai Evidence Brief

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0ZSUyRmFpJTJGcG9zdF9haV9ldmlkZW5jZV9icmllZg

Evidence Brief. Local console route POST /api/v1/ai/evidence-brief on synthetic data; advisory only. The hosted demo answers 503 hosted_demo_disabled here: it makes no provider calls.

:information_source: **Note** This endpoint does not require authentication.

```go
PostAiEvidenceBrief(
    ctx context.Context,
    body models.AiBriefHttpRequest) (
    models.ApiResponse[models.AiBriefResponse],
    error)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`models.AiBriefHttpRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/ai-brief-http-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

This method returns an [`ApiResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/sdk-infrastructure/utilities/apiresponse.md) instance. The `Data` property of this instance returns the response data which is of type [models.AiBriefResponse](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/ai-brief-response.md).


# Example Usage

```go
ctx := context.Background()

body := models.AiBriefHttpRequest{
    Stage:   models.StageEnum_VELOCITYGUARD,
}

apiResponse, err := aiController.PostAiEvidenceBrief(ctx, body)
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



