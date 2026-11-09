# Post Guide Turn

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0ZSUyRmd1aWRlJTJGcG9zdF9ndWlkZV90dXJu

Guide Turn. Local console route POST /api/v1/guide/turn on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```php
function postGuideTurn(GuideTurnRequest $body): GuideStateResponse
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`GuideTurnRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/guide-turn-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`GuideStateResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/guide-state-response.md)


# Example Usage

```php
$body = GuideTurnRequestBuilder::init(
    'text4'
)->build();

$guideController = $client->getGuideController();

try {
    $result = $guideController->postGuideTurn($body);
    echo 'GuideStateResponse:';
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



