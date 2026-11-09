# Post Aup Category Signal

Source: http://localhost:3000/#/php/x-redirect/JTI0ZSUyRmF1cCUyRnBvc3RfYXVwX2NhdGVnb3J5X3NpZ25hbA

Aup Category Signal. Local console route POST /api/v1/aup/category-signal on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```php
function postAupCategorySignal(AupCategorySignalRequest $body): AupCategorySignalResponse
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`AupCategorySignalRequest`](http://localhost:3000/llms-pages/php/models/structures/aup-category-signal-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`AupCategorySignalResponse`](http://localhost:3000/llms-pages/php/models/structures/aup-category-signal-response.md)


# Example Usage

```php
$body = AupCategorySignalRequestBuilder::init(
    'description4',
    'evaluation_id0'
)->build();

$aupController = $client->getAupController();

try {
    $result = $aupController->postAupCategorySignal($body);
    echo 'AupCategorySignalResponse:';
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



