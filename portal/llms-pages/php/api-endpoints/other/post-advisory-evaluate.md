# Post Advisory Evaluate

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0ZSUyRm90aGVyJTJGcG9zdF9hZHZpc29yeV9ldmFsdWF0ZQ

Advisory Evaluate. Local console route POST /api/v1/advisory/evaluate on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```php
function postAdvisoryEvaluate(AdvisoryRequest $body): AdvisoryEvaluationResponse
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`AdvisoryRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/advisory-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`AdvisoryEvaluationResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/advisory-evaluation-response.md)


# Example Usage

```php
$body = AdvisoryRequestBuilder::init(
    'as_of2',
    'candidate_json2',
    102,
    ThemeEnum::DISPUTE_MEDIATION
)->build();

$otherController = $client->getOtherController();

try {
    $result = $otherController->postAdvisoryEvaluate($body);
    echo 'AdvisoryEvaluationResponse:';
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



