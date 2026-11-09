# Get Paypal Status

Source: https://jiarong0423.github.io/payguard-ai/portal/#/typescript/x-redirect/JTI0ZSUyRnBheXBhbCUyRmdldF9wYXlwYWxfc3RhdHVz

Paypal Status. Local console route GET /api/v1/paypal/status on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```ts
async getPaypalStatus(
  requestOptions?: RequestOptions
): Promise<ApiResponse<PaypalStatusResponse>>
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `requestOptions` | `RequestOptions \| undefined` | Optional | Pass additional request options. |


# Response Type

**200**: Successful Response

This method returns an [`ApiResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/sdk-infrastructure/utilities/apiresponse.md) instance. The `result` property of this instance returns the response data which is of type [`PaypalStatusResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/structures/paypal-status-response.md).


# Example Usage

```ts
try {
  const response = await paypalController.getPaypalStatus();

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
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyError`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/typescript/models/exceptions/error-body.md) |



