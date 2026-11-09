# Post Guide Review

Source: http://localhost:3000/#/php/x-redirect/JTI0ZSUyRmd1aWRlJTJGcG9zdF9ndWlkZV9yZXZpZXc

Guide Review. Local console route POST /api/v1/guide/review on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```php
function postGuideReview(GuideReviewRequest $body): GuideStateResponse
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`GuideReviewRequest`](http://localhost:3000/llms-pages/php/models/structures/guide-review-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`GuideStateResponse`](http://localhost:3000/llms-pages/php/models/structures/guide-state-response.md)


# Example Usage

```php
$body = GuideReviewRequestBuilder::init()
    ->confirm(false)
    ->build();

$guideController = $client->getGuideController();

try {
    $result = $guideController->postGuideReview($body);
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
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/php/models/exceptions/error-body.md) |
| 422 | Validation Error | [`HTTPValidationErrorException`](http://localhost:3000/llms-pages/php/models/exceptions/http-validation-error.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/php/models/exceptions/error-body.md) |



