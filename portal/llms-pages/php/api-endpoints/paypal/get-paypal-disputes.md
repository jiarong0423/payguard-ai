# Get Paypal Disputes

Source: http://localhost:3000/#/php/x-redirect/JTI0ZSUyRnBheXBhbCUyRmdldF9wYXlwYWxfZGlzcHV0ZXM

List Disputes. Local console route GET /api/v1/paypal/disputes on synthetic data; advisory only.

:information_source: **Note** This endpoint does not require authentication.

```php
function getPaypalDisputes(): DisputeListResponse
```


# Response Type

**200**: Successful Response

[`DisputeListResponse`](http://localhost:3000/llms-pages/php/models/structures/dispute-list-response.md)


# Example Usage

```php
$paypalController = $client->getPaypalController();

try {
    $result = $paypalController->getPaypalDisputes();
    echo 'DisputeListResponse:';
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
| 401 | A valid demo session is required (session_required). | [`ErrorBodyException`](http://localhost:3000/llms-pages/php/models/exceptions/error-body.md) |
| 429 | Too many requests; the body says when to retry. | [`ErrorBodyException`](http://localhost:3000/llms-pages/php/models/exceptions/error-body.md) |



