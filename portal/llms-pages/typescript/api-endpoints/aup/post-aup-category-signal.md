# Post Aup Category Signal

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0ZSUyRmF1cCUyRnBvc3RfYXVwX2NhdGVnb3J5X3NpZ25hbA

Aup Category Signal. Local console route POST /api/v1/aup/category-signal on synthetic data; advisory only.

```ts
async postAupCategorySignal(
  body: AupCategorySignalRequest,
  requestOptions?: RequestOptions
): Promise<ApiResponse<AupCategorySignalResponse>>
```


# Authentication

This endpoint requires [DemoCsrf](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/getting-started/how-to-get-started/authorization.md) **AND** [DemoSession](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/getting-started/how-to-get-started/authorization.md)


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`AupCategorySignalRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/aup-category-signal-request.md) | Body, Required | JSON body for: Aup Category Signal. |
| `requestOptions` | `RequestOptions \| undefined` | Optional | Pass additional request options. |


# Response Type

**200**: Successful Response

This method returns an [`ApiResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/sdk-infrastructure/utilities/apiresponse.md) instance. The `result` property of this instance returns the response data which is of type [`AupCategorySignalResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/aup-category-signal-response.md).


# Example Usage

```ts
const body: AupCategorySignalRequest = {
  description: 'example',
  evaluationId: 'examplexxxxxxxxxxxxxxxxxxxxxxxxx',
};

try {
  const response = await aupController.postAupCategorySignal(body);

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
    }
  }
}
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyError`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/exceptions/error-body.md) |
| 403 | Origin missing or not allowed, or the CSRF token is wrong (origin_required, origin_rejected, csrf_rejected). | [`ErrorBodyError`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/exceptions/error-body.md) |
| 422 | The request does not match the accepted contract (schema_invalid). | [`ErrorBodyError`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyError`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/exceptions/error-body.md) |



