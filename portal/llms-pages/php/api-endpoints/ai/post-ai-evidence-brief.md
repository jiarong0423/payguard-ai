# Post Ai Evidence Brief

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0ZSUyRmFpJTJGcG9zdF9haV9ldmlkZW5jZV9icmllZg

Evidence Brief. Local console route POST /api/v1/ai/evidence-brief on synthetic data; advisory only. The hosted demo answers 503 hosted_demo_disabled here: it makes no provider calls.

:information_source: **Note** This endpoint does not require authentication.

```php
function postAiEvidenceBrief(AiBriefHttpRequest $body): AiBriefResponse
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`AiBriefHttpRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/ai-brief-http-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`AiBriefResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/ai-brief-response.md)


# Example Usage

```php
$body = AiBriefHttpRequestBuilder::init(
    StageEnum::VELOCITY_GUARD
)->build();

$aiController = $client->getAiController();

try {
    $result = $aiController->postAiEvidenceBrief($body);
    echo 'AiBriefResponse:';
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



