# Post Aup Acknowledge

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0ZSUyRmF1cCUyRnBvc3RfYXVwX2Fja25vd2xlZGdl

Acknowledge Aup. Local console route POST /api/v1/aup/acknowledge on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```php
function postAupAcknowledge(AupAcknowledgeRequest $body): AupAcknowledgeResponse
```


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`AupAcknowledgeRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/aup-acknowledge-request.md) | Body, Required | - |


# Response Type

**200**: Successful Response

[`AupAcknowledgeResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/aup-acknowledge-response.md)


# Example Usage

```php
$body = AupAcknowledgeRequestBuilder::init(
    ChoiceEnum::CANCEL,
    'description_digest4',
    'evaluation_id0'
)->build();

$aupController = $client->getAupController();

try {
    $result = $aupController->postAupAcknowledge($body);
    echo 'AupAcknowledgeResponse:';
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



