# Post Aup Product Reference Confirm

Source: http://localhost:3000/#/php/x-redirect/JTI0ZSUyRmF1cCUyRnBvc3RfYXVwX3Byb2R1Y3RfcmVmZXJlbmNlX2NvbmZpcm0

Aup Product Confirm. Local console route POST /api/v1/aup/product-reference/confirm on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```php
function postAupProductReferenceConfirm(ProductConfirmRequest $body): ProductConfirmResponse
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`ProductConfirmRequest`](http://localhost:3000/llms-pages/php/models/structures/product-confirm-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`ProductConfirmResponse`](http://localhost:3000/llms-pages/php/models/structures/product-confirm-response.md)


# Example Usage

```php
$body = ProductConfirmRequestBuilder::init(
    'description4',
    'evaluation_id0',
    'String3'
)->build();

$aupController = $client->getAupController();

try {
    $result = $aupController->postAupProductReferenceConfirm($body);
    echo 'ProductConfirmResponse:';
    var_dump($result);
} catch (ErrorBodyException $exp) {
    echo 'Caught ErrorBodyException:', $exp;
} catch (HTTPValidationErrorException $exp) {
    echo 'Caught HTTPValidationErrorException:', $exp;
} catch (ApiException $exp) {
    echo 'Caught:', $exp;
}
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/php/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](http://localhost:3000/llms-pages/php/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/php/models/exceptions/error-body.md) |



