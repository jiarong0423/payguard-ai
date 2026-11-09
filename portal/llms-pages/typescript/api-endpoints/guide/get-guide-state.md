# Get Guide State

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0ZSUyRmd1aWRlJTJGZ2V0X2d1aWRlX3N0YXRl

Guide State. Local console route GET /api/v1/guide/state on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```ts
async getGuideState(
  scenario?: GetGuideStateScenario,
  requestOptions?: RequestOptions
): Promise<ApiResponse<GuideStateResponse>>
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `scenario` | [`GetGuideStateScenario \| undefined`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/oneof-anyof-definitions/get-guide-state-scenario.md) | Query, Optional | This is a container for any-of cases. |
| `requestOptions` | `RequestOptions \| undefined` | Optional | Pass additional request options. |


# Response Type

**200**: Successful Response

This method returns an [`ApiResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/sdk-infrastructure/utilities/apiresponse.md) instance. The `result` property of this instance returns the response data which is of type [`GuideStateResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/guide-state-response.md).


# Example Usage

```ts
try {
  const response = await guideController.getGuideState();

  // Extracting fully parsed response body.
  console.log(response.result);

  // Extracting response status code.
  console.log(response.statusCode);
  // Extracting response headers.
  console.log(response.headers);
  // Extracting response body of type `string | Stream`
  console.log(response.body);
} catch (error) {
  if (error instanceof ApiError) {
    // Extracting response error status code.
    console.log(error.statusCode);
    // Extracting response error headers.
    console.log(error.headers);
    // Extracting response error body of type `string | Stream`.
    console.log(error.body);
    if (error instanceof ErrorBodyError) {
      console.log(error.result);
    } else if (error instanceof HTTPValidationError) {
      console.log(error.result);
    }
  }
}
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyError`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationError`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyError`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/exceptions/error-body.md) |



