# Post Cases Route

Source: https://jiarong0423.github.io/payguard-ai/portal/#/php/x-redirect/JTI0ZSUyRm90aGVyJTJGcG9zdF9jYXNlc19yb3V0ZQ

Case Route. Local console route POST /api/v1/cases/route on synthetic data; advisory only.

```php
function postCasesRoute(CaseRouteRequest $body): CaseRouteResponse
```


# Authentication

This endpoint requires [DemoCsrf](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/getting-started/how-to-get-started/authorization.md) **AND** [DemoSession](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/getting-started/how-to-get-started/authorization.md)


# Parameters

| Parameter | Type | Tags | Description |
|  --- | --- | --- | --- |
| `body` | [`CaseRouteRequest`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/case-route-request.md) | Body, Required | JSON body for: Case Route. |


# Response Type

**200**: Successful Response

[`CaseRouteResponse`](https://jiarong0423.github.io/payguard-ai/portal/llms-pages/php/models/structures/case-route-response.md)


# Example Usage

```php
$body = CaseRouteRequestBuilder::init(
    'handmade ceramic coffee mug'
)->build();

$otherController = $client->getOtherController();

try {
    $result = $otherController->postCasesRoute($body);
    echo 'CaseRouteResponse:';
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



