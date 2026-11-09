# Get Guide State

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0ZSUyRmd1aWRlJTJGZ2V0X2d1aWRlX3N0YXRl

Guide State. Local console route GET /api/v1/guide/state on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```go
GetGuideState(
    ctx context.Context,
    scenario *models.GetGuideStateScenario) (
    models.ApiResponse[models.GuideStateResponse],
    error)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `scenario` | [`*models.GetGuideStateScenario`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/oneof-anyof-definitions/get-guide-state-scenario.md) | Query, Optional | This is a container for any-of cases. |


# Response Type

**200**: Successful Response

This method returns an [`ApiResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/sdk-infrastructure/utilities/apiresponse.md) instance. The `Data` property of this instance returns the response data which is of type [models.GuideStateResponse](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/guide-state-response.md).


# Example Usage

```go
ctx := context.Background()

apiResponse, err := guideController.GetGuideState(ctx, nil)
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



