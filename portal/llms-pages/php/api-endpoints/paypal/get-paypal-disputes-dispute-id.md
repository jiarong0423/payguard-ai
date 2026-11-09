# Get Paypal Disputes Dispute Id

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0ZSUyRnBheXBhbCUyRmdldF9wYXlwYWxfZGlzcHV0ZXNfZGlzcHV0ZV9pZA

Get Dispute. Local console route GET /api/v1/paypal/disputes/{dispute_id} on synthetic data; advisory only.

```php
function getPaypalDisputesDisputeId(string $disputeId): DisputeDetailResponse
```


# Authentication

This endpoint requires [DemoSession](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/getting-started/how-to-get-started/authorization.md)


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `disputeId` | `string` | Template, Required | Dispute id. |


# Response Type

**200**: Successful Response

[`DisputeDetailResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/dispute-detail-response.md)


# Example Usage

```php
$disputeId = 'PP-R-BNP-XXXX7173';

$paypalController = $client->getPaypalController();

try {
    $result = $paypalController->getPaypalDisputesDisputeId($disputeId);
    echo 'DisputeDetailResponse:';
    var_dump($result);
} catch (ErrorBodyException $exp) {
    echo 'Caught ErrorBodyException:', $exp;
} catch (ApiException $exp) {
    echo 'Caught:', $exp;
}
```


# Errors

| HTTP Status Code | Error Description | Exception Class |
|  --- | --- | --- |
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/exceptions/error-body.md) |
| 422 | The request does not match the accepted contract (schema_invalid). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/exceptions/error-body.md) |



