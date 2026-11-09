# Post Policy Assess

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0ZSUyRm90aGVyJTJGcG9zdF9wb2xpY3lfYXNzZXNz

Policy Assess. Local console route POST /api/v1/policy/assess on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```php
function postPolicyAssess(PolicyRequest $body): PolicyAssessmentResponse
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`PolicyRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/policy-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`PolicyAssessmentResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/policy-assessment-response.md)


# Example Usage

```php
$body = PolicyRequestBuilder::init(
    'as_of2',
    102,
    ThemeEnum::DISPUTE_MEDIATION
)->build();

$otherController = $client->getOtherController();

try {
    $result = $otherController->postPolicyAssess($body);
    echo 'PolicyAssessmentResponse:';
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



