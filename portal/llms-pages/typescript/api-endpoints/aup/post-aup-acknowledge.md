# Post Aup Acknowledge

Source: http://localhost:3000/#/typescript/x-redirect/JTI0ZSUyRmF1cCUyRnBvc3RfYXVwX2Fja25vd2xlZGdl

Acknowledge Aup. Local console route POST /api/v1/aup/acknowledge on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```ts
async postAupAcknowledge(
  body: AupAcknowledgeRequest,
  requestOptions?: RequestOptions
): Promise<ApiResponse<AupAcknowledgeResponse>>
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`AupAcknowledgeRequest`](http://localhost:3000/llms-pages/typescript/models/structures/aup-acknowledge-request.md) | Body, Required | - |
| `requestOptions` | `RequestOptions \| undefined` | Optional | Pass additional request options. |


# Response Type

**200**: Successful Response

This method returns an [`ApiResponse`](http://localhost:3000/llms-pages/typescript/sdk-infrastructure/utilities/apiresponse.md) instance. The `result` property of this instance returns the response data which is of type [`AupAcknowledgeResponse`](http://localhost:3000/llms-pages/typescript/models/structures/aup-acknowledge-response.md).


# Example Usage

```ts
const body: AupAcknowledgeRequest = {
  choice: ChoiceEnum.CANCEL,
  descriptionDigest: 'description_digest4',
  evaluationId: 'evaluation_id0',
};

try {
  const response = await aupController.postAupAcknowledge(body);

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



