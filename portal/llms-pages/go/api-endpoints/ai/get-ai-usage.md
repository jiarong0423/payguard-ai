# Get Ai Usage

Source: https://jiarong0423.github.io/payguard-ai/portal/#/go/x-redirect/JTI0ZSUyRmFpJTJGZ2V0X2FpX3VzYWdl

(optimise r24) This session's AI calls: stage, model, tokens, latency, estimated cost. No prompt or reply
text is ever stored; the hosted demo makes no model call and answers an empty list.

```go
GetAiUsage(
    ctx context.Context) (
    models.ApiResponse[models.AiUsageResponse],
    error)
```


# Authentication

This endpoint requires [DemoSession](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/getting-started/how-to-get-started/authorization.md)


# Response Type

**200**: Successful Response

This method returns an [`ApiResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/sdk-infrastructure/utilities/apiresponse.md) instance. The `Data` property of this instance returns the response data which is of type [models.AiUsageResponse](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/structures/ai-usage-response.md).


# Example Usage

```go
ctx := context.Background()

apiResponse, err := aiController.GetAiUsage(ctx)
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


# Example Response *(as JSON)*

```json
{
  "cost_note": "example",
  "entries": [
    {
      "at": "example",
      "latency_ms": 0,
      "outcome": "ok",
      "stage": "source_compliance"
    }
  ],
  "price_table_source": "example",
  "source": "session_memory"
}
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/go/models/exceptions/error-body.md) |



