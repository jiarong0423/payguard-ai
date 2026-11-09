# Post References Search

Source: http://localhost:3000/#/go/x-redirect/JTI0ZSUyRnJlZmVyZW5jZXMlMkZwb3N0X3JlZmVyZW5jZXNfc2VhcmNo

References. Local console route POST /api/v1/references/search on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```go
PostReferencesSearch(
    ctx context.Context,
    body models.ReferenceRequest) (
    models.ApiResponse[models.ReferenceResponse],
    error)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`models.ReferenceRequest`](http://localhost:3000/llms-pages/go/models/structures/reference-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

This method returns an [`ApiResponse`](http://localhost:3000/llms-pages/go/sdk-infrastructure/utilities/apiresponse.md) instance. The `Data` property of this instance returns the response data which is of type [models.ReferenceResponse](http://localhost:3000/llms-pages/go/models/structures/reference-response.md).


# Example Usage

```go
ctx := context.Background()

body := models.ReferenceRequest{
    CaseStage:              models.ToPointer(models.CaseStage2Enum_ANY),
    Jurisdiction:           "US",
    Limit:                  models.ToPointer(3),
    Query:                  "query6",
    RequireKnownSourceDate: models.ToPointer(false),
    Theme:                  models.ThemeEnum_DISPUTEMEDIATION,
}

apiResponse, err := referencesController.PostReferencesSearch(ctx, body)
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



