# Post Aup Review

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0ZSUyRmF1cCUyRnBvc3RfYXVwX3Jldmlldw

Aup. Local console route POST /api/v1/aup/review on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```php
function postAupReview(AupRequest $body): AupResponse
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`AupRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/aup-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`AupResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/aup-response.md)


# Example Usage

```php
$body = AupRequestBuilder::init(
    'description4'
)->build();

$aupController = $client->getAupController();

try {
    $result = $aupController->postAupReview($body);
    echo 'AupResponse:';
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
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/exceptions/error-body.md) |



