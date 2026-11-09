# Post Aup Product Reference Confirm

Source: https://jiarong0423.github.io/payguard-ai/portal/#/python/x-redirect/JTI0ZSUyRmF1cCUyRnBvc3RfYXVwX3Byb2R1Y3RfcmVmZXJlbmNlX2NvbmZpcm0

Aup Product Confirm. Local console route POST /api/v1/aup/product-reference/confirm on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```python
def post_aup_product_reference_confirm(self,
                                      body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`ProductConfirmRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/product-confirm-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`ProductConfirmResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/structures/product-confirm-response.md)


# Example Usage

```python
body = ProductConfirmRequest(
    description='description4',
    evaluation_id='evaluation_id0',
    product_id='String3'
)

result = aup_controller.post_aup_product_reference_confirm(body)
print(result)
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/python/models/exceptions/error-body.md) |



