# Post Aup Product Reference

Source: http://localhost:3000/#/python/x-redirect/JTI0ZSUyRmF1cCUyRnBvc3RfYXVwX3Byb2R1Y3RfcmVmZXJlbmNl

Aup Product Reference. Local console route POST /api/v1/aup/product-reference on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```python
def post_aup_product_reference(self,
                              body)
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`ProductReferenceRequest`](http://localhost:3000/llms-pages/python/models/structures/product-reference-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`ProductReferenceResponse`](http://localhost:3000/llms-pages/python/models/structures/product-reference-response.md)


# Example Usage

```python
body = ProductReferenceRequest(
    description='description4',
    evaluation_id='evaluation_id0'
)

result = aup_controller.post_aup_product_reference(body)
print(result)
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/python/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](http://localhost:3000/llms-pages/python/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/python/models/exceptions/error-body.md) |



