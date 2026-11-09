# Post Studio Agent Turn

Source: http://localhost:3000/#/go/x-redirect/JTI0ZSUyRnN0dWRpbyUyRnBvc3Rfc3R1ZGlvX2FnZW50X3R1cm4

Studio Agent Turn. Local console route POST /api/v1/studio/agent-turn on synthetic data; advisory only. The hosted demo answers 503 hosted_demo_disabled here: it makes no provider calls.

:information_source: **Note** This endpoint does not require authentication.

```go
PostStudioAgentTurn(
    ctx context.Context,
    body interface{}) (
    models.ApiResponse[interface{}],
    error)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | `interface{}` | Body, Required | - |


# Response Type

**200**: Successful Response

This method returns an [`ApiResponse`](http://localhost:3000/llms-pages/go/sdk-infrastructure/utilities/apiresponse.md) instance. The `Data` property of this instance returns the response data which is of type interface{}.


# Example Usage

```go
ctx := context.Background()

body := interface{}("[key1, val1][key2, val2]")

apiResponse, err := studioController.PostStudioAgentTurn(ctx, body)
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
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/go/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](http://localhost:3000/llms-pages/go/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/go/models/exceptions/error-body.md) |



