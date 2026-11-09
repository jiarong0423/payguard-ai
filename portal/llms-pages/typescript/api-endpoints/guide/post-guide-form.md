# Post Guide Form

Source: http://localhost:3000/#/typescript/x-redirect/JTI0ZSUyRmd1aWRlJTJGcG9zdF9ndWlkZV9mb3Jt

Guide Form. Local console route POST /api/v1/guide/form on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```ts
async postGuideForm(
  body: GuideFormRequest,
  requestOptions?: RequestOptions
): Promise<ApiResponse<GuideStateResponse>>
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`GuideFormRequest`](http://localhost:3000/llms-pages/typescript/models/structures/guide-form-request.md) | Body, Required | - |
| `requestOptions` | `RequestOptions \| undefined` | Optional | Pass additional request options. |


# Response Type

**200**: Successful Response

This method returns an [`ApiResponse`](http://localhost:3000/llms-pages/typescript/sdk-infrastructure/utilities/apiresponse.md) instance. The `result` property of this instance returns the response data which is of type [`GuideStateResponse`](http://localhost:3000/llms-pages/typescript/models/structures/guide-state-response.md).


# Example Usage

```ts
const body: GuideFormRequest = {
  confirmReview: false,
};

try {
  const response = await guideController.postGuideForm(body);

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
| 401 | A valid demo session is required (session_required). | [`ErrorBodyError`](http://localhost:3000/llms-pages/typescript/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationError`](http://localhost:3000/llms-pages/typescript/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyError`](http://localhost:3000/llms-pages/typescript/models/exceptions/error-body.md) |



