# Get Demo State

Source: http://localhost:3000/#/go/x-redirect/JTI0ZSUyRmRlbW8lMkZnZXRfZGVtb19zdGF0ZQ

State. Local console route GET /api/v1/demo/state on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```go
GetDemoState(
    ctx context.Context) (
    models.ApiResponse[models.StateResponse],
    error)
```


# Response Type

**200**: Successful Response

This method returns an [`ApiResponse`](http://localhost:3000/llms-pages/go/sdk-infrastructure/utilities/apiresponse.md) instance. The `Data` property of this instance returns the response data which is of type [models.StateResponse](http://localhost:3000/llms-pages/go/models/structures/state-response.md).


# Example Usage

```go
ctx := context.Background()

apiResponse, err := demoController.GetDemoState(ctx)
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
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/go/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/go/models/exceptions/error-body.md) |



