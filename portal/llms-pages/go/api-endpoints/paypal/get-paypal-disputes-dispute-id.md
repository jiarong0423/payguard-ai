# Get Paypal Disputes Dispute Id

Source: http://localhost:3000/#/go/x-redirect/JTI0ZSUyRnBheXBhbCUyRmdldF9wYXlwYWxfZGlzcHV0ZXNfZGlzcHV0ZV9pZA

Get Dispute. Local console route GET /api/v1/paypal/disputes/{dispute_id} on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```go
GetPaypalDisputesDisputeId(
    ctx context.Context,
    disputeId string) (
    models.ApiResponse[models.DisputeDetailResponse],
    error)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `disputeId` | `string` | Template, Required | Dispute id. |


# Response Type

**200**: Successful Response

This method returns an [`ApiResponse`](http://localhost:3000/llms-pages/go/sdk-infrastructure/utilities/apiresponse.md) instance. The `Data` property of this instance returns the response data which is of type [models.DisputeDetailResponse](http://localhost:3000/llms-pages/go/models/structures/dispute-detail-response.md).


# Example Usage

```go
ctx := context.Background()

disputeId := "dispute_id2"

apiResponse, err := paypalController.GetPaypalDisputesDisputeId(ctx, disputeId)
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



