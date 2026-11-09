# Post Disputes Case Ref Draft

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0ZSUyRm90aGVyJTJGcG9zdF9kaXNwdXRlc19jYXNlX3JlZl9kcmFmdA

Draft. Local console route POST /api/v1/disputes/{case_ref}/draft on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```ts
async postDisputesCaseRefDraft(
  caseRef: string,
  body: unknown,
  requestOptions?: RequestOptions
): Promise<ApiResponse<DisputeDraftResponse>>
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `caseRef` | `string` | Template, Required | Case ref. |
| `body` | `unknown` | Body, Required | - |
| `requestOptions` | `RequestOptions \| undefined` | Optional | Pass additional request options. |


# Response Type

**200**: Successful Response

This method returns an [`ApiResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/sdk-infrastructure/utilities/apiresponse.md) instance. The `result` property of this instance returns the response data which is of type [`DisputeDraftResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/dispute-draft-response.md).


# Example Usage

```ts
const caseRef = 'case_ref4';

const body = { 'key1': 'val1', 'key2': 'val2' };

try {
  const response = await otherController.postDisputesCaseRefDraft(
    caseRef,
    body
  );

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



