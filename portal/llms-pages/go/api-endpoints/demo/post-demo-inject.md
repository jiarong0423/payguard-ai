# Post Demo Inject

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0ZSUyRmRlbW8lMkZwb3N0X2RlbW9faW5qZWN0

Inject. Local console route POST /api/v1/demo/inject on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```go
PostDemoInject(
    ctx context.Context,
    body models.InjectRequest) (
    models.ApiResponse[models.StateResponse],
    error)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`models.InjectRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/inject-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

This method returns an [`ApiResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/sdk-infrastructure/utilities/apiresponse.md) instance. The `Data` property of this instance returns the response data which is of type [models.StateResponse](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/state-response.md).


# Example Usage

```go
ctx := context.Background()

body := models.InjectRequest{
    Scenario: models.Scenario5Enum_DISPUTE,
}

apiResponse, err := demoController.PostDemoInject(ctx, body)
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



