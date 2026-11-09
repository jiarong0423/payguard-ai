# Post Guide Review

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0ZSUyRmd1aWRlJTJGcG9zdF9ndWlkZV9yZXZpZXc

Guide Review. Local console route POST /api/v1/guide/review on synthetic data; advisory only.

```go
PostGuideReview(
    ctx context.Context,
    body models.GuideReviewRequest) (
    models.ApiResponse[models.GuideStateResponse],
    error)
```


# Authentication

This endpoint requires [DemoCsrf](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/getting-started/how-to-get-started/authorization.md) **AND** [DemoSession](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/getting-started/how-to-get-started/authorization.md)


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`models.GuideReviewRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/guide-review-request.md) | Body, Required | JSON body for: Guide Review. |


# Response Type

**200**: Successful Response

This method returns an [`ApiResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/sdk-infrastructure/utilities/apiresponse.md) instance. The `Data` property of this instance returns the response data which is of type [models.GuideStateResponse](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/guide-state-response.md).


# Example Usage

```go
ctx := context.Background()

body := models.GuideReviewRequest{
}

apiResponse, err := guideController.PostGuideReview(ctx, body)
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



