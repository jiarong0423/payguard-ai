# Post Paypal Disputes Provide Evidence

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0ZSUyRnBheXBhbCUyRnBvc3RfcGF5cGFsX2Rpc3B1dGVzX3Byb3ZpZGVfZXZpZGVuY2U

Provide Evidence. Local console route POST /api/v1/paypal/disputes/provide-evidence on synthetic data; advisory only. The hosted demo answers 503 hosted_demo_disabled here: it makes no provider calls.

```php
function postPaypalDisputesProvideEvidence(ProvideEvidenceRequest $body): ProvideEvidenceResponse
```


# Authentication

This endpoint requires [DemoCsrf](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/getting-started/how-to-get-started/authorization.md) **AND** [DemoSession](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/getting-started/how-to-get-started/authorization.md)


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`ProvideEvidenceRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/provide-evidence-request.md) | Body, Required | JSON body for: Provide Evidence. |


# Response Type

**200**: Successful Response

[`ProvideEvidenceResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/provide-evidence-response.md)


# Example Usage

```php
$body = ProvideEvidenceRequestBuilder::init(
    'case-ref-001',
    'PP-R-BNP-XXXX7173'
)
    ->submit(false)
    ->build();

$paypalController = $client->getPaypalController();

try {
    $result = $paypalController->postPaypalDisputesProvideEvidence($body);
    echo 'ProvideEvidenceResponse:';
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
| 403 | Origin missing or not allowed, or the CSRF token is wrong (origin_required, origin_rejected, csrf_rejected). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/exceptions/error-body.md) |
| 422 | The request does not match the accepted contract (schema_invalid). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/exceptions/error-body.md) |
| 503 | Hosted demo only: this route makes no provider call (hosted_demo_disabled). | [`ErrorBodyException`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/exceptions/error-body.md) |



